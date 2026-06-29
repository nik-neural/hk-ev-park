# ⚡ 香港 EV 泊車

全香港 EV 停車場搜尋 — 即時空位、地圖、附近 EV 站。

[![開啟 Web App](https://img.shields.io/badge/開啟-Web_App-059669?style=for-the-badge)](https://nik-neural.github.io/hk-ev-park/)

## 功能

- 全港 EV 停車場地圖搜尋
- 即時空位狀態一目了然
- 地區篩選 + 附近 EV 站
- 可加入主畫面，離線快取（Service Worker）

## 加入主畫面（PWA）

1. 用手機或電腦開啟上方連結
2. **Safari / Chrome** → 分享 / 選單 → **加入主畫面**

## 同系列 App

| | App | 說明 | 連結 |
|---|-----|------|------|
| 🚌 | **巴士到站** | 九巴 / 城巴 ETA + 天氣 | [nik-neural.github.io/hk-bus](https://nik-neural.github.io/hk-bus/) |
| 💰 | **圓子基金** | 群組消費記帳 + 圓子基金 | [nik-neural.github.io/circle-fund](https://nik-neural.github.io/circle-fund/) |
| ⚡ | **香港 EV 泊車** | 全港 EV 停車場即時空位 | [nik-neural.github.io/hk-ev-park](https://nik-neural.github.io/hk-ev-park/) |

## 技術

- 單一 HTML · Tailwind CDN · Leaflet 地圖
- [GitHub Pages](https://pages.github.com/) 部署
- PWA（`manifest.webmanifest` + `icons/` + `sw.js`）