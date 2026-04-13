"""
Drama产出物唯一性测试
"""
import pytest

class TestDramaArtifacts:
    """产出物唯一性测试"""
    
    def test_unique_artifacts_per_milestone(self, sample_drama_task):
        """测试每个里程碑独立产出物"""
        if not sample_drama_task:
            pytest.skip("无Drama任务")
        
        milestone_artifacts = {}
        for m in sample_drama_task['milestones']:
            if m.get('status') == 'completed':
                artifacts = m.get('execution_details', {}).get('artifacts', [])
                milestone_artifacts[m['id']] = [a.get('name', '') for a in artifacts]
        
        # 检查每个里程碑至少有1个产出物
        for ms_id, artifact_names in milestone_artifacts.items():
            assert len(artifact_names) > 0, \
                f"{ms_id}无产出物"
        
        # 检查不同里程碑产出物名称不同
        all_names = []
        for names in milestone_artifacts.values():
            all_names.extend(names)
        
        unique_names = set(all_names)
        # 允许相同类型产出物（如TXT），但检查是否有明显重复
        duplicate_threshold = len(milestone_artifacts)
        assert len(all_names) - len(unique_names) < duplicate_threshold, \
            f"产出物重复过多：{len(all_names)}个产出物中只有{len(unique_names)}个唯一"
    
    def test_all_artifacts_downloadable(self, sample_drama_task):
        """测试所有产出物可下载"""
        if not sample_drama_task:
            pytest.skip("无Drama任务")
        
        import subprocess
        failed_downloads = []
        
        for m in sample_drama_task['milestones']:
            if m.get('status') == 'completed':
                artifacts = m.get('execution_details', {}).get('artifacts', [])
                for a in artifacts:
                    url = a.get('url', '')
                    if url and len(url) > 10:
                        result = subprocess.run(
                            ['curl', '-s', '-I', '-o', '/dev/null', url],
                            capture_output=True, text=True
                        )
                        if 'HTTP/1.1 200' not in result.stdout:
                            failed_downloads.append(a.get('name', ''))
        
        assert len(failed_downloads) == 0, \
            f"以下产出物下载失败: {', '.join(failed_downloads)}"