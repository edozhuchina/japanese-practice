# 日语口语练习

一个 Django + 纯前端（HTML/JS）的日语口语学习 Web 应用。提供 12 个实用场景、34 句日语对话，支持 J
LPT 等级筛选、学习进度追踪、Web Speech 语音朗读等功能。

## 技术栈

| 层 | 技术 |
|---|---|
| 后端 | Django 4.2 + Django REST Framework + Simple JWT |
| 前端 | 原生 HTML5 + CSS3 + Vanilla JS |
| 数据库 | SQLite（开发环境） |
| 语音 | Web Speech API（浏览器内置） |

## 快速启动

### 1. 启动后端服务器

```bash
cd /Users/zhuqiupingchinaicloud.com/Desktop/jp-test/projects/japanese-practice
source venv/bin/activate

# 首次运行：加载场景数据
python manage.py load_scenes

# 启动后端（默认端口 8001）
python manage.py runserver 0.0.0.0:8001
```

### 2. 启动前端服务器

```bash
cd frontend
python3 -m http.server 5500
```

浏览器访问 `http://localhost:5500`。

> **注意**：确保后端端口（`8001`）与前端 `auth.js` 中的 `API_BASE_URL` 一致。

### 3. 访问系统

| 地址 | 用途 |
|---|---|
| `http://localhost:5500` | 前端首页 |
| `http://localhost:5500/login.html` | 登录页 |
| `http://localhost:5500/register.html` | 注册页 |
| `http://localhost:5500/scenes.html` | 场景大厅 |
| `http://localhost:5500/practice.html?id=1` | 对话练习 |
| `http://127.0.0.1:8001/admin/` | 管理员后台 |

## 功能一览

- 🔐 **用户系统**：注册、登录（JWT）、个人资料管理
- 🗺️ **场景大厅**：12 个场景按分类和 JLPT 等级筛选
- 📖 **对话练习**：逐句导航，含日文/假名注音/罗马音/中文翻译
- 🔊 **语音朗读**：浏览器内置 Web Speech API 朗读日语（支持 Safari/Chrome）
- ⭐ **难点标记**：标记常忘的对话，跟踪学习进度
- 📊 **进度追踪**：后端持久化记录每个场景的学习进度
- 🎭 **核心词汇**：点击对话气泡展开词汇卡片

## 项目结构

```
japanese-practice/
├── config/              # Django 项目配置
│   ├── settings.py      # 核心配置（CORS、JWT、用户模型等）
│   ├── urls.py          # 路由配置
│   └── wsgi.py
├── users/               # 用户模块
│   ├── models.py        # 自定义 User 模型（日语等级、学习目标）
│   ├── views.py         # 注册、登录、Token 刷新、个人资料 API
│   ├── serializers.py   # 用户序列化器
│   └── admin.py         # 用户后台管理
├── scenes/              # 场景模块
│   ├── models.py        # Scene、Dialogue、StudyProgress 模型
│   ├── views.py         # 场景列表/详情、进度、完成 API
│   ├── serializers.py   # 对话和进度序列化器
│   ├── fixtures/        # 初始场景数据（12场景 34句对话）
│   └── management/      # load_scenes 数据加载命令
├── frontend/            # 前端页面
│   ├── index.html       # 首页（欢迎+跳转场景大厅）
│   ├── login.html       # 登录页
│   ├── register.html    # 注册页
│   ├── scenes.html      # 场景大厅（分类+等级筛选）
│   ├── practice.html    # 对话练习页（朗读+词汇+进度）
│   └── js/
│       └── auth.js      # 登录/注册/Token 刷新核心逻辑
└── manage.py
```

## API 接口

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/api/users/register/` | 用户注册 |
| POST | `/api/users/login/` | 用户登录（返回 JWT） |
| POST | `/api/users/token/refresh/` | Token 刷新 |
| GET | `/api/users/profile/` | 获取/修改个人资料 |
| GET | `/api/scenes/` | 场景列表（可选 `?category=` `?level=`） |
| GET | `/api/scenes/<id>/` | 场景详情（含全部对话） |
| GET | `/api/scenes/progress/?scene_id=` | 获取场景学习进度 |
| POST | `/api/scenes/complete/` | 标记对话完成 |

## 管理员后台

访问 `http://127.0.0.1:8001/admin/` 使用以下账号：

- 用户名：`admin`
- 密码：`admin123`

在后台可以管理用户、场景、对话和学习进度。

## 常见问题

**Q: 前端无法调用后端 API？**
确保前后端端口与 `settings.py` 中 `CORS_ALLOWED_ORIGINS` 匹配。

**Q: 语音朗读没有声音？**
- 仅支持 Chrome 或 Safari
- 系统必须安装日语语音（macOS 默认包含：系统偏好设置 → 语音 → 语音库 → 下载日语）

**Q: 修改端口？**
修改 `frontend/js/auth.js` 中的 `API_BASE_URL` 和 `SCENES_API_URL` 以匹配后端端口。
