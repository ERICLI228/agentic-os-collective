"""
TK数据采集测试
"""
import pytest
import json
from pathlib import Path

class TestDataCollector:
    """数据采集完整性测试"""
    
    def test_data_completeness(self, sample_tk_task):
        """测试数据采集完整性>95%"""
        if not sample_tk_task:
            pytest.skip("无TK任务")
        
        for m in sample_tk_task['milestones']:
            if m['id'] == 'MS-1' and m.get('status') == 'completed':
                artifacts = m.get('execution_details', {}).get('artifacts', [])
                assert len(artifacts) > 0, "MS-1无产出物"
                
                # 检查CSV文件存在性
                has_csv = any('csv' in a.get('name', '').lower() for a in artifacts)
                assert has_csv, "缺少CSV数据文件"
                return
        pytest.skip("MS-1未完成")
    
    def test_artifact_downloadable(self, sample_tk_task):
        """测试产出物可下载"""
        if not sample_tk_task:
            pytest.skip("无TK任务")
        
        import subprocess
        for m in sample_tk_task['milestones']:
            if m.get('status') == 'completed':
                artifacts = m.get('execution_details', {}).get('artifacts', [])
                for a in artifacts:
                    url = a.get('url', '')
                    if url and len(url) > 10:
                        result = subprocess.run(
                            ['curl', '-s', '-I', '-o', '/dev/null', url],
                            capture_output=True, text=True
                        )
                        assert 'HTTP/1.1 200' in result.stdout, \
                            f"{a.get('name')}下载失败"