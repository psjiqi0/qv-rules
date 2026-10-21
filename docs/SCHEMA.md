# 国家包 JSON Schema

每个 `countries/<CC>.json` 是一个国家包，描述「用户以该国为所在国」时的分流规则。

```json
{
  "country": "CN",
  "name": "中国",
  "version": 1,
  "direct_domains": ["example.cn"],
  "direct_cidrs": [],
  "groups": {
    "ai":       {"direct": ["..."], "proxy": ["..."], "default_exit": "auto"},
    "video":    {"direct": [], "proxy": [], "default_exit": "auto"},
    "chat":     {"direct": [], "proxy": [], "default_exit": "auto"},
    "shopping": {"direct": [], "proxy": [], "default_exit": "auto"},
    "finance":  {"direct": [], "proxy": [], "default_exit": "auto"},
    "games":    {"direct": [], "proxy": [], "default_exit": "auto"}
  }
}
```

## 字段语义

| 字段 | 含义 |
|---|---|
| `country` | 国家码（ISO 3166-1 alpha-2 大写），与文件名一致 |
| `name` | 国家显示名（中文） |
| `version` | 国家包自身版本号（整数，内容变更时 +1） |
| `direct_domains` | 顶层直连域名集：归不进六大分组的该国国内服务域名，命中走直连 |
| `direct_cidrs` | 直连 IP 段（CIDR 形式）。可为空，如 CN 包留空，chnroute 由 App 内置提供 |
| `groups.<组>.direct` | 该分组内走直连的服务域名 |
| `groups.<组>.proxy` | 该分组内走代理的服务域名 |
| `groups.<组>.default_exit` | 该分组代理流的默认出口（见下） |

六大分组固定为：`ai`、`video`、`chat`、`shopping`、`finance`、`games`。

## 域名与匹配语义

- 域名一律写**后缀形式**：不带 `*.`、不带协议头、不带路径，如 `qq.com`、`youtube.com`。
- 匹配为后缀逐级匹配：规则 `qq.com` 命中 `qq.com` 本身及任意子域（如 `wx.qq.com`）。
- 条目之间允许冗余（子域条目被父域覆盖时无害）。

## default_exit 取值

| 值 | 含义 |
|---|---|
| `"auto"` | 自动：走客户端优选出的当前最优节点 |
| 国家码，如 `"US"` | 该分组的代理流默认钉到该国家的节点（用户可在 App 内覆盖） |
| `"direct"` | 该分组默认全部直连（其 `proxy` 列一般应为空） |

用户在 App 内对某个分组的出口选择（自动 / 指定节点）优先于本文件的 `default_exit`。

## 判定顺序（客户端执行，命中即止）

1. 用户自定义规则（App 内手填名单，最高优先）
2. 分组规则：域名先查六大分组的 `direct` / `proxy` 列
3. 所在国直连集：`direct_domains` 域名后缀、`direct_cidrs` IP 段（含 App 内置 chnroute 兜底）
4. DNS 解析缓存判定（域名解析结果的历史判定）
5. 兜底：未命中一律走代理（fail-closed，宁可绕远不误直连）

例外：局域网/私有地址、VPN 服务器自身 IP 永远直连，不受上述顺序影响。
