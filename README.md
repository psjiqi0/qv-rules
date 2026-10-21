# qv-rules — QV 分流规则库

QV 客户端的分流规则数据源：按国家维护「国家包」，每个国家包包含该国的直连域名集，
以及 AI / 视频 / 聊天 / 购物 / 金融 / 游戏六大分组的直连/代理服务名单与默认出口。

本仓库只含公开的域名/IP 段数据，**不含任何密钥、凭证或用户数据**。

## 结构

```
meta.json            版本与各国文件索引（App 先拉它判新旧）
countries/<CC>.json  国家包，如 countries/CN.json
docs/SCHEMA.md       国家包 JSON 格式说明（字段语义、判定顺序）
tools/build_meta.py  扫 countries/ 重新生成 meta.json
```

## App 拉取方式

生效流程：客户端先用内置基础规则连上 VPN → 拉 `meta.json` → 版本更新才下载所在国国家包 →
sha256 校验通过后原子替换缓存并自动启用；失败保留旧版。

- Raw（主）:
  - `https://raw.githubusercontent.com/psjiqi0/qv-rules/main/meta.json`
  - `https://raw.githubusercontent.com/psjiqi0/qv-rules/main/countries/CN.json`
- jsDelivr 镜像（兜底）:
  - `https://cdn.jsdelivr.net/gh/psjiqi0/qv-rules@main/meta.json`
  - `https://cdn.jsdelivr.net/gh/psjiqi0/qv-rules@main/countries/CN.json`

## 更新方式

1. 直接编辑 `countries/<CC>.json`（格式见 `docs/SCHEMA.md`），或新增国家包文件。
2. 跑 `python3 tools/build_meta.py` 重新生成 `meta.json`（含文件 sha256 与域名总条数）。
3. 一并提交推送。客户端下次拉取时按 `meta.version` 判断并自动更新。

## 说明

- CN 包的 `direct_cidrs` 留空：中国 IP 段表（chnroute，4000+ 条）体积较大，
  仍由 App 内置 assets 提供；本仓库的国家包先只承载域名规则，后续国家可按需内嵌 CIDR。
- 域名均为后缀形式（不带 `*.`、不带协议头），按后缀逐级匹配。
