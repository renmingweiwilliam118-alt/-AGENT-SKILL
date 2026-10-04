#!/bin/bash
# 技能一键恢复脚本
# 用法: bash restore.sh [目标 Hermes 路径]
# 默认恢复到当前用户的 Hermes

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_HERMES="${1:-$HOME/AppData/Local/hermes}"

echo "=== 技能恢复脚本 ==="
echo "源: $SCRIPT_DIR"
echo "目标: $TARGET_HERMES"
echo ""

# 检查源目录
if [ ! -d "$SCRIPT_DIR" ]; then
    echo "❌ 源目录不存在: $SCRIPT_DIR"
    exit 1
fi

# 创建目标目录
mkdir -p "$TARGET_HERMES/skills"

# 复制所有技能（排除缓存和临时文件）
echo "正在复制技能..."
for dir in "$SCRIPT_DIR"/*/; do
    skill_name=$(basename "$dir")
    if [ -d "$dir" ]; then
        # 排除非技能目录
        if [[ "$skill_name" == ".git" ]] || [[ "$skill_name" == "__pycache__" ]]; then
            continue
        fi
        cp -r "$dir" "$TARGET_HERMES/skills/" 2>/dev/null || true
        echo "  ✓ $skill_name"
    fi
done ""

echo ""
echo "=== 恢复完成 ==="
echo "共恢复 $(find "$TARGET_HERMES/skills" -name "SKILL.md" | wc -l) 个技能"
echo ""
echo "重启 Hermes 后生效。"
