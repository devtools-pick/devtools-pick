# Codex Task: 批量重写所有文章

## 背景
我有一个 AI 开发者工具评测网站 (https://devtools-pick.vercel.app)，需要你帮我重写所有文章，提升质量。

## 需要重写的文件

### Reviews (3篇)
1. ~/Hermes/ai-tools-site/src/content/reviews/github-copilot-review.md
2. ~/Hermes/ai-tools-site/src/content/reviews/jetbrains-ai-review.md
3. ~/Hermes/ai-tools-site/src/content/reviews/chatgpt-review.md

### Comparisons (3篇)
4. ~/Hermes/ai-tools-site/src/content/comparisons/cursor-vs-github-copilot.md
5. ~/Hermes/ai-tools-site/src/content/comparisons/claude-vs-chatgpt-coding.md
6. ~/Hermes/ai-tools-site/src/content/comparisons/chatgpt-vs-claude-vs-gemini.md

### Alternatives (2篇)
7. ~/Hermes/ai-tools-site/src/content/alternatives/github-copilot-alternatives.md
8. ~/Hermes/ai-tools-site/src/content/alternatives/best-midjourney-alternatives.md

### Best Of (5篇)
9. ~/Hermes/ai-tools-site/src/content/bestof/best-ai-coding-assistants.md
10. ~/Hermes/ai-tools-site/src/content/bestof/best-free-ai-code-assistants.md
11. ~/Hermes/ai-tools-site/src/content/bestof/best-ai-writing-tools-developers.md
12. ~/Hermes/ai-tools-site/src/content/bestof/best-ai-api-platforms.md
13. ~/Hermes/ai-tools-site/src/content/bestof/best-ai-monitoring-tools.md

## 重写要求

对每个文件：
1. 读取原文
2. 按照以下标准重写
3. 直接覆盖原文件

## 质量标准

### 必须做到
- 像真人写的（有个人观点、使用体验）
- 具体的使用场景和例子
- 承认工具的局限性
- 句子长短混用
- 800-1500字
- 保留 YAML frontmatter 不变
- 保留 ## AFFILIATE_LINK ## 占位符
- 保留 Related Articles 部分
- 包含 FAQ 部分

### 永远不用
- crucial, leverage, delve, vibrant, robust, seamless, comprehensive
- Let's dive in, Here's what you need to know
- The future looks bright
- Great question!, Excellent point!
- It is important to note that

### 参考样本
~/Hermes/ai-tools-site/src/content/reviews/cursor-review.md（已由 GPT-5.5 重写，作为质量标准）

## 执行方式
请一个一个文件处理，每个文件重写后直接覆盖保存。
