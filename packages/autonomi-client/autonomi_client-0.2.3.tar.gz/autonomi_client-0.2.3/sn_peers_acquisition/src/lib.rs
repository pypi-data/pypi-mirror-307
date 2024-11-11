// Copyright 2024 MaidSafe.net limited.
//
// This SAFE Network Software is licensed to you under The General Public License (GPL), version 3.
// Unless required by applicable law or agreed to in writing, the SAFE Network Software distributed
// under the GPL Licence is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied. Please review the Licences for the specific language governing
// permissions and limitations relating to use of the SAFE Network Software.

pub mod error;

use crate::error::{Error, Result};
use clap::Args;
#[cfg(feature = "network-contacts")]
use lazy_static::lazy_static;
use libp2p::{multiaddr::Protocol, Multiaddr};
use rand::{seq::SliceRandom, thread_rng};
use reqwest::Client;
use std::time::Duration;
use tracing::*;
use url::Url;

#[cfg(feature = "network-contacts")]
lazy_static! {
    // URL containing the multi-addresses of the bootstrap nodes.
    pub static ref NETWORK_CONTACTS_URL: String =
       "https://sn-testnet.s3.eu-west-2.amazonaws.com/network-contacts".to_string();
}

// The maximum number of retries to be performed while trying to get peers from a URL.
const MAX_RETRIES_ON_GET_PEERS_FROM_URL: usize = 7;

/// The name of the environment variable that can be used to pass peers to the node.
pub const SAFE_PEERS_ENV: &str = "SAFE_PEERS";

#[derive(Args, Debug, Default, Clone)]
pub struct PeersArgs {
    /// Set to indicate this is the first node in a new network
    ///
    /// If this argument is used, any others will be ignored because they do not apply to the first
    /// node.
    #[clap(long)]
    pub first: bool,
    /// Peer(s) to use for bootstrap, in a 'multiaddr' format containing the peer ID.
    ///
    /// A multiaddr looks like
    /// '/ip4/1.2.3.4/tcp/1200/tcp/p2p/12D3KooWRi6wF7yxWLuPSNskXc6kQ5cJ6eaymeMbCRdTnMesPgFx' where
    /// `1.2.3.4` is the IP, `1200` is the port and the (optional) last part is the peer ID.
    ///
    /// This argument can be provided multiple times to connect to multiple peers.
    ///
    /// Alternatively, the `SAFE_PEERS` environment variable can provide a comma-separated peer
    /// list.
    #[clap(long = "peer", env = "SAFE_PEERS", value_name = "multiaddr", value_delimiter = ',', value_parser = parse_peer_addr, conflicts_with = "first")]
    pub peers: Vec<Multiaddr>,

    /// Specify the URL to fetch the network contacts from.
    ///
    /// This argument will be overridden if the "peers" argument is set or if the `local`
    /// feature flag is enabled.
    #[cfg(feature = "network-contacts")]
    #[clap(long, conflicts_with = "first")]
    pub network_contacts_url: Option<Url>,
}

impl PeersArgs {
    /// Gets the peers based on the arguments provided.
    ///
    /// If the `--first` flag is used, no peers will be provided.
    ///
    /// Otherwise, peers are obtained in the following order of precedence:
    /// * The `--peer` argument.
    /// * The `SAFE_PEERS` environment variable.
    /// * Using the `local` feature, which will return an empty peer list.
    /// * Using the `network-contacts` feature, which will download the peer list from a file on S3.
    ///
    /// Note: the current behaviour is that `--peer` and `SAFE_PEERS` will be combined. Some tests
    /// currently rely on this. We will change it soon.
    pub async fn get_peers(self) -> Result<Vec<Multiaddr>> {
        self.get_peers_inner(false).await
    }

    /// Gets the peers based on the arguments provided.
    ///
    /// If the `--first` flag is used, no peers will be provided.
    ///
    /// Otherwise, peers are obtained in the following order of precedence:
    /// * The `--peer` argument.
    /// * The `SAFE_PEERS` environment variable.
    /// * Using the `local` feature, which will return an empty peer list.
    ///
    /// This will not fetch the peers from network-contacts even if the `network-contacts` feature is enabled. Use
    /// get_peers() instead.
    ///
    /// Note: the current behaviour is that `--peer` and `SAFE_PEERS` will be combined. Some tests
    /// currently rely on this. We will change it soon.
    pub async fn get_peers_exclude_network_contacts(self) -> Result<Vec<Multiaddr>> {
        self.get_peers_inner(true).await
    }

    async fn get_peers_inner(self, skip_network_contacts: bool) -> Result<Vec<Multiaddr>> {
        if self.first {
            info!("First node in a new network");
            return Ok(vec![]);
        }

        let mut peers = if !self.peers.is_empty() {
            info!("Using peers supplied with the --peer argument(s) or SAFE_PEERS");
            self.peers
        } else if cfg!(feature = "local") {
            info!("No peers given");
            info!("The `local` feature is enabled, so peers will be discovered through mDNS.");
            return Ok(vec![]);
        } else if skip_network_contacts {
            info!("Skipping network contacts");
            return Ok(vec![]);
        } else if cfg!(feature = "network-contacts") {
            self.get_network_contacts().await?
        } else {
            vec![]
        };

        if peers.is_empty() {
            error!("Peers not obtained through any available options");
            return Err(Error::PeersNotObtained);
        };

        // Randomly sort peers before we return them to avoid overly hitting any one peer
        let mut rng = thread_rng();
        peers.shuffle(&mut rng);

        Ok(peers)
    }

    // should not be reachable, but needed for the compiler to be happy.
    #[expect(clippy::unused_async)]
    #[cfg(not(feature = "network-contacts"))]
    async fn get_network_contacts(&self) -> Result<Vec<Multiaddr>> {
        Ok(vec![])
    }

    #[cfg(feature = "network-contacts")]
    async fn get_network_contacts(&self) -> Result<Vec<Multiaddr>> {
        let url = self
            .network_contacts_url
            .clone()
            .unwrap_or(Url::parse(NETWORK_CONTACTS_URL.as_str())?);

        info!("Trying to fetch the bootstrap peers from {url}");

        get_peers_from_url(url).await
    }
}

/// Parse strings like `1.2.3.4:1234` and `/ip4/1.2.3.4/tcp/1234` into a multiaddr.
pub fn parse_peer_addr(addr: &str) -> std::result::Result<Multiaddr, libp2p::multiaddr::Error> {
    // Parse valid IPv4 socket address, e.g. `1.2.3.4:1234`.
    if let Ok(addr) = addr.parse::<std::net::SocketAddrV4>() {
        let start_addr = Multiaddr::from(*addr.ip());

        // Turn the address into a `/ip4/<ip>/udp/<port>/quic-v1` multiaddr.
        #[cfg(not(feature = "websockets"))]
        let multiaddr = start_addr
            .with(Protocol::Udp(addr.port()))
            .with(Protocol::QuicV1);

        // Turn the address into a `/ip4/<ip>/udp/<port>/websocket-websys-v1` multiaddr.
        #[cfg(feature = "websockets")]
        let multiaddr = start_addr
            .with(Protocol::Tcp(addr.port()))
            .with(Protocol::Ws("/".into()));

        return Ok(multiaddr);
    }

    // Parse any valid multiaddr string
    addr.parse::<Multiaddr>()
}

/// Get and parse a list of peers from a URL. The URL should contain one multiaddr per line.
pub async fn get_peers_from_url(url: Url) -> Result<Vec<Multiaddr>> {
    let mut retries = 0;

    #[cfg(not(target_arch = "wasm32"))]
    let request_client = Client::builder().timeout(Duration::from_secs(10)).build()?;
    // Wasm does not have the timeout method yet.
    #[cfg(target_arch = "wasm32")]
    let request_client = Client::builder().build()?;

    loop {
        let response = request_client.get(url.clone()).send().await;

        match response {
            Ok(response) => {
                let mut multi_addresses = Vec::new();
                if response.status().is_success() {
                    let text = response.text().await?;
                    trace!("Got peers from url: {url}: {text}");
                    // example of contacts file exists in resources/network-contacts-examples
                    for addr in text.split('\n') {
                        // ignore empty/last lines
                        if addr.is_empty() {
                            continue;
                        }

                        debug!("Attempting to parse {addr}");
                        multi_addresses.push(parse_peer_addr(addr)?);
                    }
                    if !multi_addresses.is_empty() {
                        trace!("Successfully got peers from URL {multi_addresses:?}");
                        return Ok(multi_addresses);
                    } else {
                        return Err(Error::NoMultiAddrObtainedFromNetworkContacts(
                            url.to_string(),
                        ));
                    }
                } else {
                    retries += 1;
                    if retries >= MAX_RETRIES_ON_GET_PEERS_FROM_URL {
                        return Err(Error::FailedToObtainPeersFromUrl(
                            url.to_string(),
                            MAX_RETRIES_ON_GET_PEERS_FROM_URL,
                        ));
                    }
                }
            }
            Err(err) => {
                error!("Failed to get peers from URL {url}: {err:?}");
                retries += 1;
                if retries >= MAX_RETRIES_ON_GET_PEERS_FROM_URL {
                    return Err(Error::FailedToObtainPeersFromUrl(
                        url.to_string(),
                        MAX_RETRIES_ON_GET_PEERS_FROM_URL,
                    ));
                }
            }
        }
        trace!(
            "Failed to get peers from URL, retrying {retries}/{MAX_RETRIES_ON_GET_PEERS_FROM_URL}"
        );
        tokio::time::sleep(Duration::from_secs(1)).await;
    }
}
