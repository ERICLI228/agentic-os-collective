"""
TK里程碑产出物测试
"""
import pytest
import json

class TestMilestoneArtifacts:
    """里程碑产出物完整性测试"""
    
    def test_all_milestones_have_artifacts(self, sample_tk_task):
        """测试所有里程碑都有产出物"""
        if not sample_tk_task:
            pytest.skip("无TK任务")
        
        for m in sample_tk_task['milestones']:
            if m.get('status') == 'completed':
                artifacts = m.get('execution_details', {}).get('artifacts', [])
                assert len(artifacts) > 0, \
                    f"{m['id']}无产出物"
    
    def test_no_duplicate_artifacts(self, sample_tk_task):
        """测试无重复产出物"""
        if not sample_tk_task:
            pytest.skip("无TK任务")
        
        all_urls = []
        for m in sample_tk_task['milestones']:
            artifacts = m.get('execution_details', {}).get('artifacts', [])
            for a in artifacts:
                url = a.get('url', '')
                if url:
                    all_urls.append(url)
        
        unique_urls = set(all_urls)
        assert len(all_urls) == len(unique_urls), \
            f"发现{len(all_urls) - len(unique_urls)}个重复产出物"
    
    def test_file_size_above_threshold(self, sample_tk_task):
        """测试文件大小>1000字节"""
        if not sample_tk_task:
            pytest.skip("无TK任务")
        
        import subprocess
        for m in sample_tk_task['milestones']:
            if m.get('status') == 'completed':
                artifacts = m.get('execution_details', {}).get('artifacts', [])
                for a in artifacts:
                    url = a.get('url', '')
                    if url and len(url) > 10:
                        # 检查Content-Length
                        result = subprocess.run(
                            ['curl', '-s', '-I', url],
                            capture_output=True, text=True
                        )
                        for line in result.stdout.split('\n'):
                            if 'Content-Length:' in line:
                                size = int(line.split(':')[1].strip())
                                assert size >= 1000, \
                                    f"{a.get('name')}大小{size}字节<1000"