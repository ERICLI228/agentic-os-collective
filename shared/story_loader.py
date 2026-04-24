#!/usr/bin/env python3
"""
故事配置加载器 (v1.0)
从 stories/*.yaml 加载故事配置，替代所有硬编码数据

用法:
  from shared.story_loader import load_story
  story = load_story("shuihuzhuan")   # 水浒传
  story = load_story("sanguo")        # 三国演义
  story = load_story("xiyou")         # 西游记

  # 访问数据
  story.name           # "水浒传"
  story.role("武松")   # Role namedtuple
  story.episodes       # [Episode, ...]
  story.scenes         # {name: description}
  story.controversies  # [ControversyRule, ...]
"""
import yaml
from pathlib import Path
from typing import Optional, List
from collections import namedtuple

STORIES_DIR = Path(__file__).parent.parent / "stories"

Role = namedtuple("Role", ["id", "name", "traits", "voice_style", "tts_voice", "description", "default_scene"])
Episode = namedtuple("Episode", ["id", "title", "chapter", "character", "score", "tags"])
ControversyRule = namedtuple("ControversyRule", ["id", "pattern", "severity", "problem", "rewrite", "keep"])


class Story:
    """故事配置对象"""

    def __init__(self, data: dict):
        self._data = data
        self.name: str = data["name"]
        self.id: str = data["id"]
        self.genre: str = data.get("genre", "")
        self.era: str = data.get("era", "")
        self.style: str = data.get("style", "默认")
        self.description: str = data.get("description", "")

        # 提示词模板
        self.system_prompt: str = data.get("system_prompt", "")
        self.script_prompt: str = data.get("script_prompt", "")
        self.video_prompt: str = data.get("video_prompt", "")

        # 筛选标准
        self.selection_criteria: dict = data.get("selection_criteria", {})

        # 角色列表
        self._roles: dict = {}
        self._roles_by_name: dict = {}
        for r in data.get("roles", []):
            role = Role(**{k: r.get(k, "") for k in Role._fields})
            self._roles[role.id] = role
            self._roles_by_name[role.name] = role

        # 剧集列表
        self.episodes: List[Episode] = []
        for e in data.get("episodes", []):
            self.episodes.append(Episode(**{k: e.get(k, 0 if k == "score" else [] if k == "tags" else "") for k in Episode._fields}))

        # 场景
        self.scenes: dict = data.get("scenes", {})

        # 争议规则
        self.controversies: List[ControversyRule] = []
        for c in data.get("controversy_rules", []):
            self.controversies.append(ControversyRule(**{k: c.get(k, "") for k in ControversyRule._fields}))

        # 争议规则字典 (按 id 索引)
        self._controversies_by_id: dict = {c.id: c for c in self.controversies}
        self._controversies_by_pattern: dict = {c.pattern: c for c in self.controversies}

    def role(self, name: str) -> Optional[Role]:
        """按角色名或 ID 查找"""
        return self._roles_by_name.get(name) or self._roles.get(name)

    def roles(self) -> List[Role]:
        return list(self._roles.values())

    def episode(self, episode_id: str) -> Optional[Episode]:
        for e in self.episodes:
            if e.id == episode_id:
                return e
        return None

    def controversy(self, key: str) -> Optional[ControversyRule]:
        """按 id 或 pattern 查找争议规则"""
        return self._controversies_by_id.get(key) or self._controversies_by_pattern.get(key)

    def __repr__(self):
        return f"Story({self.id}: {self.name}, {len(self._roles)} roles, {len(self.episodes)} episodes)"


def load_story(story_id: str) -> Story:
    """加载故事配置"""
    yaml_path = STORIES_DIR / f"{story_id}.yaml"
    if not yaml_path.exists():
        raise FileNotFoundError(f"故事配置不存在: {yaml_path} (可用: {list_available()})")

    with open(yaml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return Story(data)


def list_available() -> list:
    """列出所有可用的故事 ID"""
    return sorted(f.stem for f in STORIES_DIR.glob("*.yaml"))


if __name__ == "__main__":
    print("📚 可用故事:")
    for sid in list_available():
        story = load_story(sid)
        print(f"  {story.id:15s} → {story.name:8s} | {story.genre} | {len(story.episodes)} 集 | {len(story.roles())} 角色 | {len(story.controversies)} 争议规则")
