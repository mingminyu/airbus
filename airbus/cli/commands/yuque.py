import requests
from typing import Text, List
from airbus.decorators import progressbar

from rich.progress import track


class ObtainYuqueDocs(object):
    """Get all urls public docs of special account"""
    def __init__(
            self,
            token: Text = None,
            uid: Text = None,
            ):
        self.headers = {"X-Auth-Token": token}
        self.uid = uid

    def __get_repos(self) -> List[Text]:
        """Get all public repos of special account"""
        repo_api = f"https://www.yuque.com/api/v2/users/{self.uid}/repos"
        res = requests.get(repo_api, headers=self.headers).json()
        repos = [repo['slug'] for repo in res['data'] if repo['public'] == 1]

        return repos

    @progressbar
    def get_docs(self) -> List[Text]:
        docs = []
        repos = self.__get_repos()
        yield len(repos)

        for idx, repo in enumerate(repos):
            docs_api = f"https://www.yuque.com/api/v2/repos/{self.uid}/{repo}/docs"
            doc_url = "https://www.yuque.com/{uid}/{repo}/{doc_url}"
            res = requests.get(docs_api, headers=self.headers).json()
            docs_repo = [doc_url.format(uid=self.uid, repo=repo, doc_url=doc['slug'])
                            for doc in res['data'] if doc['public'] == 1]
            docs += docs_repo
            yield idx + 1

        return docs


def check(args):
    pass

def thumbsup(args):
    """Thumbs up docs by other yuque accounts"""
    if args.token and args.uid:
        docs = ObtainYuqueDocs(token=args.token, uid=args.uid)
    else:
        raise Exception("``")

    pass

def follow(args):
    """Follow other yuque users"""
    pass

def unfollow(args):
    """Unfollow other yuque users"""
    pass


def review(args):
    """Review other docs, not your own docs"""
    pass

def shorthand(args):
    """Review other docs, not your own docs"""
    pass