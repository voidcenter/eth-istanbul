import requests


class LensProtocolAPI:
    API_URL = 'https://api-v2.lens.dev/'

    def get_profiles(self, user_addresses: list[str]):

        body = """
    query {
      profiles (request: {
        limit: Fifty
        where: {
          ownedBy: [""" + ",".join([f'"{addr}"' for addr in user_addresses]) + """]
          #   handles: [
          #   "lens/aavegrants",
          #   "lens/gmoney"
          # ]
        }
      } ) {
        items {
          id
          ownedBy {
            address
            chainId
          }
          txHash
          createdAt
          stats {
            id
            followers
            following
            comments
            posts
            mirrors
            quotes
            publications
            reactions
            reactionsUpVote: reactions(request: {type: UPVOTE})
            reactionsDownVote: reactions(request: {type: DOWNVOTE})
            reacted
            reactedUpVote: reactions(request: {type: UPVOTE})
            reactedDownVote: reactions(request: {type: DOWNVOTE})
            countOpenActions
          }
          operations {
            id
            canBlock
            canUnblock
            canFollow
            canUnfollow
          }
          interests
          guardian {
            protected
            cooldownEndsOn
          }
          invitedBy {
            id
            ownedBy {
              address
              chainId
            }
          }
          invitesLeft
          onchainIdentity {
            proofOfHumanity
            ens {
              name
            }
            sybilDotOrg {
              verified
              source {
                twitter {
                  handle
                }
              }
            }
            worldcoin {
              isHuman
            }
          }
          followNftAddress {
            address
            chainId
          }
          metadata {
            displayName
            bio
            rawURI
            appId
            coverPicture {
              raw {
                mimeType
                width
                height
                uri
              }
            }
          }
          handle {
            id
            fullHandle
            namespace
            localName
            linkedTo {
              contract {
                address
                chainId
              }
              nftTokenId
            }
            ownedBy
          }
          signless
          sponsor
        }
      }
    }
        """
        return self._make_request(body)

    def _make_request(self, body):
        response = requests.post(url=self.API_URL, json={"query": body})
        # print("response status code: ", response.status_code)
        if response.status_code == 200:
            # print("response : ", response.json())
            return response.json()
        else:
            raise Exception(f"failed with {response.text}")

    def get_followers(self, profile_id, cursor=None):
        body = """
        query {
          followers (request: { 
            of: """ + f'"{profile_id}"' + """
            limit: Fifty
            cursor: """ + ("null" if cursor is None else f'"{cursor}"') + """}) {
            items {
              id
              ownedBy {
                address
                chainId
              }
            }
            pageInfo {
              next
            }
          }
        }
        """
        # print(body)
        return self._make_request(body)


if __name__ == '__main__':
    lens = LensProtocolAPI()

    res = lens.get_profiles([
        "0xc1f2b71A502B551a65Eee9C96318aFdD5fd439fA",
    ])
    print(res)
    print(res["data"]["profiles"]["items"][0]["stats"]["followers"])
    print(res["data"]["profiles"]["items"][0]["onchainIdentity"]["worldcoin"]["isHuman"])

    # lens.get_followers("0xeB1c22baACAFac7836f20f684C946228401FF01C")
