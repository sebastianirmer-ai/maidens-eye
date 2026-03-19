"""
Data parser for The Archstones RPCS3 server player count data.

Parses raw text data from the server and extracts player counts per location.
"""

import re
from collections import Counter


class OnlineUsersParser:
    """Parses raw text file with player counts from The Archstones server.
    
    The server provides data in format like:
    - "3 5-2 Swamp 2" (3 players in area "5-2 Swamp 2")
    - "1 Nexus" (1 player in "Nexus")
    """
    
    def parse(self, text: str) -> dict:
        """Parse the raw text file with player counts.
        
        Args:
            text: Raw text content from the server
            
        Returns:
            Dictionary containing:
            - total: Total number of players online
            - sections: Dict mapping location names to player counts (sorted by count)
            - raw_lines: List of original text lines
            
        Example:
            >>> parser = OnlineUsersParser()
            >>> result = parser.parse("3 5-2 Swamp\\n1 Nexus\\n")
            >>> result['total']
            4
            >>> result['sections']
            {'5-2 Swamp': 3, 'Nexus': 1}
        """
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        
        sections = Counter()
        total = 0
        
        # Parse lines in format: "3 5-2 Swamp 2" or "1 Nexus"
        for line in lines:
            match = re.match(r'^(\d+)\s+(.+?)\s*$', line)
            if match:
                count = int(match.group(1))
                location = match.group(2).strip()
                sections[location] += count
                total += count
        
        # Sort by player count (descending), then alphabetically
        sorted_sections = dict(sorted(sections.items(), key=lambda kv: (-kv[1], kv[0])))
        
        return {
            "total": total,
            "sections": sorted_sections,
            "raw_lines": lines,
        }
