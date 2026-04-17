from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class Proposal:
    id: str
    creator: str
    title: str
    description: str
    votes_for: int
    votes_against: int
    status: str

class DAOGovernance:
    def __init__(self, token_contract):
        self.token = token_contract
        self.proposals: Dict[str, Proposal] = {}
        self.voters: Dict[str, List[str]] = {}

    def create_proposal(self, proposal_id: str, creator: str, title: str, desc: str) -> bool:
        if self.token.balance_of(creator) < 10:
            return False
        self.proposals[proposal_id] = Proposal(
            id=proposal_id,
            creator=creator,
            title=title,
            description=desc,
            votes_for=0,
            votes_against=0,
            status="active"
        )
        return True

    def vote(self, proposal_id: str, voter: str, support: bool) -> bool:
        if proposal_id not in self.proposals or self.proposals[proposal_id].status != "active":
            return False
        if voter in self.voters.get(proposal_id, []):
            return False
        power = int(self.token.balance_of(voter))
        prop = self.proposals[proposal_id]
        if support:
            prop.votes_for += power
        else:
            prop.votes_against += power
        if proposal_id not in self.voters:
            self.voters[proposal_id] = []
        self.voters[proposal_id].append(voter)
        return True

    def finalize_proposal(self, proposal_id: str) -> bool:
        if proposal_id not in self.proposals:
            return False
        prop = self.proposals[proposal_id]
        if prop.votes_for > prop.votes_against:
            prop.status = "passed"
        else:
            prop.status = "rejected"
        return True
