// 🌟 配置后端 API 的基础地址 (修改此处以匹配你的 Django 服务器端口)
const API_BASE_URL = (typeof window !== 'undefined' && window.API_BASE_URL) 
    ? window.API_BASE_URL : 'http://localhost:8000/api/users';
const SCENES_API_URL = (typeof window !== 'undefined' && window.SCENES_API_URL)
    ? window.SCENES_API_URL : 'http://localhost:8000/api/scenes';
const PROGRESS_API_URL = (typeof window !== 'undefined' && window.PROGRESS_API_URL)
    ? window.PROGRESS_API_URL : 'http://localhost:8000/api/scenes';

/**
 * Token 自动刷新机制
 */
async function refreshTokenIfNeeded() {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) return false;
    
    try {
        const response = await fetch(API_BASE_URL + '/token/refresh/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh: refreshToken })
        });
        
        if (!response.ok) throw new Error('Token 刷新失败');
        
        const data = await response.json();
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
        return true;
    } catch (error) {
        // Token 刷新失败，清除登录状态并跳转登录页
        logout();
        return false;
    }
}

/**
 * 1. 登录逻辑
 */
async function handleLogin(username, password) {
    try {
        const response = await fetch(API_BASE_URL + '/login/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || '用户名或密码错误，请重试');
        }

        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
        localStorage.setItem('user_info', JSON.stringify(data.user));

        return { success: true, message: `欢迎回来，${data.user.nickname || data.user.username}！` };

    } catch (error) {
        return { success: false, message: error.message };
    }
}

/**
 * 2. 注册逻辑
 */
async function handleRegister(formData) {
    try {
        const response = await fetch(API_BASE_URL + '/register/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (!response.ok) {
            const errorMsg = Object.values(data).flat().join(', ');
            throw new Error(errorMsg);
        }

        return { success: true, message: data.message };

    } catch (error) {
        return { success: false, message: error.message };
    }
}

/**
 * 3. 检查用户是否已登录
 */
function checkAuth() {
    const token = localStorage.getItem('access_token');
    const userInfo = localStorage.getItem('user_info');
    
    if (token && userInfo) {
        // 验证 token 是否过期 (简单检查)
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            const isExpired = payload.exp * 1000 < Date.now();
            if (isExpired) {
                // Token 过期，尝试刷新
                refreshTokenIfNeeded();
                return null;
            }
        } catch (e) {
            // token 解析失败，清除
            logout();
            return null;
        }
        return JSON.parse(userInfo);
    }
    return null;
}

/**
 * 4. 退出登录
 */
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_info');
    window.location.href = 'login.html';
}
