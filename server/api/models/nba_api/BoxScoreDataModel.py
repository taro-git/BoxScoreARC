from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

@dataclass
class BoxScoreData:
    data: Dict[int, List[Tuple[int, List[int]]]] = field(default_factory=lambda: defaultdict(list))
