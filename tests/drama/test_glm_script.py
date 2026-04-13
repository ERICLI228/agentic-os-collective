"""
GLM剧本生成测试
"""
import pytest
import json

class TestGLMScript:
    """剧本格式验证"""
    
    def test_script_format(self, sample_drama_task):
        """测试剧本格式正确"""
        if not sample_drama_task:
            pytest.skip("无Drama任务")
        
        for m in sample_drama_task['milestones']:
            if m['id'] == 'MS-4' and m.get('status') == 'completed':
                artifacts = m.get('execution_details', {}).get('artifacts', [])
                
                # 检查剧本文件存在
                has_script = any('script' in a.get('name', '').lower() for a in artifacts)
                assert has_script, "缺少剧本文件"
                
                # 检查文件大小
                for a in artifacts:
                    if 'script' in a.get('name', '').lower():
                        # 下载测试
                        import subprocess
                        url = a.get('url', '')
                        if url:
                            result = subprocess.run(
                                ['curl', '-s', url],
                                capture_output=True, text=True
                            )
                            script = result.stdout
                            assert len(script) >= 1000, \
                                f"剧本字数{len(script)}不足1000"
                            return
        pytest.skip("MS-4未完成")
    
    def test_script_has_scenes(self, sample_drama_task):
        """测试剧本包含场景标记"""
        if not sample_drama_task:
            pytest.skip("无Drama任务")
        
        for m in sample_drama_task['milestones']:
            if m['id'] == 'MS-4' and m.get('status') == 'completed':
                artifacts = m.get('execution_details', {}).get('artifacts', [])
                for a in artifacts:
                    if 'script' in a.get('name', '').lower():
                        url = a.get('url', '')
                        if url:
                            import subprocess
                            result = subprocess.run(
                                ['curl', '-s', url],
                                capture_output=True, text=True
                            )
                            script = result.stdout
                            scene_count = script.count("【") + script.count("幕")
                            assert scene_count >= 3, \
                                f"场景数量{scene_count}不足3个"
                            return
        pytest.skip("MS-4未完成")