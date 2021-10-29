import pytest
from collections import defaultdict
from bomapp.bom_api import create_bom, dfs
from bomapp.bom_requests import MockRequests

BOM = """{"data": [
                   {"id": 0, "parent_part_id": null, "part_id": 1, "quantity": 1},
                   {"id": 1, "parent_part_id": 1, "part_id": 2, "quantity": 2}, 
                   {"id": 2, "parent_part_id": 1, "part_id": 3, "quantity": 2}, 
                   {"id": 3, "parent_part_id": 1, "part_id": 4, "quantity": 5}, 
                   {"id": 4, "parent_part_id": 2, "part_id": 5, "quantity": 4}, 
                   {"id": 5, "parent_part_id": 3, "part_id": 6, "quantity": 3}, 
                   {"id": 6, "parent_part_id": 5, "part_id": 7, "quantity": 3}
        ]}"""

Parts = {1: 'A', 2: 'B', 3: 'C', 4: 'E', 5: 'C', 6: 'D', 7: 'D'}


def test_create():
    mock_requests = MockRequests(BOM, Parts)
    bom, root = create_bom(mock_requests)
    result_map = defaultdict(int)
    dfs(bom, result_map, root, 1)
    assert result_map['A'] == 1
    assert result_map['B'] == 2
    assert result_map['C'] == 10
    assert result_map['D'] == 30
    assert result_map['E'] == 5
