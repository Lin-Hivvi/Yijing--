/*
 * 易镜 · 模拟周易筮占系统
 * 前端JavaScript功能
 */

// 全局配置
const CONFIG = {
    apiBase: '/api',
    animationDuration: 300
};

// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', function() {
    console.log('易镜系统启动...');
    
    // 初始化所有交互组件
    initDivinationForm();
    initSearchFunctionality();
    initYaoSymbols();
    initNavigation();
    
    // 显示加载完成消息
    showNotification('易镜系统已就绪', 'success');
});

// ===== 起卦表单处理 =====
function initDivinationForm() {
    const form = document.getElementById('divination-form');
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const submitBtn = this.querySelector('.divination-btn');
        const originalText = submitBtn.innerHTML;
        
        // 显示加载状态
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 起卦中...';
        submitBtn.disabled = true;
        
        // 添加太极图加速动画
        const taiji = document.querySelector('.taiji-circle, .taiji');
        if (taiji) {
            taiji.style.animationDuration = '1s';
        }
        
        // 发送AJAX请求
        fetch(this.action, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams(new FormData(this))
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // 如果返回JSON，可以在这里处理响应
                // 如果是AJAX请求，直接跳转到结果页
                window.location.href = '/divinate';
            } else {
                throw new Error(data.error || '起卦失败');
            }
        })
        .catch(error => {
            console.error('起卦错误:', error);
            showNotification(`起卦失败：${error.message}`, 'error');
            
            // 恢复按钮状态
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
            
            // 恢复太极图动画
            if (taiji) {
                taiji.style.animationDuration = '10s';
            }
        });
    });
}

// ===== 搜索功能 =====
function initSearchFunctionality() {
    const searchInput = document.querySelector('.search-input');
    const guaItems = document.querySelectorAll('.gua-item');
    
    if (searchInput && guaItems.length > 0) {
        searchInput.addEventListener('input', debounce(function() {
            const searchTerm = this.value.trim().toLowerCase();
            
            if (searchTerm.length === 0) {
                // 显示所有项目
                guaItems.forEach(item => item.style.display = 'block');
                return;
            }
            
            let visibleCount = 0;
            guaItems.forEach(item => {
                const text = item.textContent.toLowerCase();
                const isVisible = text.includes(searchTerm);
                
                item.style.display = isVisible ? 'block' : 'none';
                if (isVisible) visibleCount++;
            });
            
            // 如果没有匹配项，显示提示
            const noResultsMsg = document.getElementById('no-results-message');
            if (visibleCount === 0) {
                if (!noResultsMsg) {
                    const message = document.createElement('div');
                    message.id = 'no-results-message';
                    message.className = 'no-results';
                    message.innerHTML = `<p>未找到匹配的卦象。请尝试其他关键词。</p>`;
                    searchInput.parentNode.appendChild(message);
                }
            } else if (noResultsMsg) {
                noResultsMsg.remove();
            }
        }, 300));
    }
    
    // 卦象点击效果
    guaItems.forEach(item => {
        item.addEventListener('click', function(e) {
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = '';
            }, 200);
        });
    });
}

// ===== 爻符号交互 =====
function initYaoSymbols() {
    const yaoSymbols = document.querySelectorAll('.yao-symbol');
    
    yaoSymbols.forEach(symbol => {
        // 鼠标悬停效果
        symbol.addEventListener('mouseenter', function() {
            if (this.classList.contains('changing-yao')) {
                this.style.boxShadow = '0 0 0 3px #fdcb6e';
            } else {
                this.style.boxShadow = '0 0 0 3px rgba(52, 152, 219, 0.3)';
            }
        });
        
        symbol.addEventListener('mouseleave', function() {
            this.style.boxShadow = '';
        });
        
        // 点击显示解释
        symbol.addEventListener('click', function() {
            const yaoNum = this.dataset.yao || '未知';
            const yaoType = this.dataset.type || '未知';
            
            showNotification(`第${yaoNum}爻：${yaoType}`, 'info');
        });
    });
}

// ===== 导航功能 =====
function initNavigation() {
    // 平滑滚动到锚点
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // 返回顶部按钮
    const backToTopBtn = document.getElementById('back-to-top');
    if (!backToTopBtn) return;
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.style.display = 'block';
        } else {
            backToTopBtn.style.display = 'none';
        }
    });
    
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// ===== 工具函数 =====

// 防抖函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func.apply(this, args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 显示通知消息
function showNotification(message, type = 'info') {
    // 移除现有的通知
    const existingNotice = document.querySelector('.global-notification');
    if (existingNotice) {
        existingNotice.remove();
    }
    
    // 创建新通知
    const notice = document.createElement('div');
    notice.className = `global-notification notification-${type}`;
    notice.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${getNotificationIcon(type)}"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close">&times;</button>
    `;
    
    // 添加到页面
    document.body.appendChild(notice);
    
    // 显示动画
    setTimeout(() => {
        notice.classList.add('show');
    }, 10);
    
    // 关闭按钮事件
    notice.querySelector('.notification-close').addEventListener('click', function() {
        notice.classList.remove('show');
        setTimeout(() => notice.remove(), 300);
    });
    
    // 自动消失（如果是成功或信息消息）
    if (type === 'success' || type === 'info') {
        setTimeout(() => {
            if (notice.parentNode) {
                notice.classList.remove('show');
                setTimeout(() => notice.remove(), 300);
            }
        }, 3000);
    }
    
    // 添加基础样式（如果不存在）
    if (!document.getElementById('notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            .global-notification {
                position: fixed;
                top: 20px;
                right: 20px;
                background: white;
                padding: 16px 24px;
                border-radius: 8px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.15);
                display: flex;
                align-items: center;
                justify-content: space-between;
                z-index: 9999;
                transform: translateX(100%);
                opacity: 0;
                transition: all 0.3s ease;
                max-width: 400px;
                border-left: 4px solid #3498db;
            }
            
            .global-notification.show {
                transform: translateX(0);
                opacity: 1;
            }
            
            .notification-success { border-left-color: #2ecc71; }
            .notification-error { border-left-color: #e74c3c; }
            .notification-warning { border-left-color: #f39c12; }
            .notification-info { border-left-color: #3498db; }
            
            .notification-content {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-right: 20px;
            }
            
            .notification-close {
                background: none;
                border: none;
                font-size: 24px;
                cursor: pointer;
                color: #7f8c8d;
                padding: 0;
                width: 24px;
                height: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 4px;
            }
            
            .notification-close:hover {
                background: #f8f9fa;
                color: #333;
            }
        `;
        document.head.appendChild(style);
    }
}

// 获取通知图标
function getNotificationIcon(type) {
    const icons = {
        'success': 'check-circle',
        'error': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// 复制文本到剪贴板
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('已复制到剪贴板', 'success');
    }).catch(err => {
        console.error('复制失败:', err);
        showNotification('复制失败', 'error');
    });
}

// 格式化日期时间
function formatDateTime(date) {
    const d = date || new Date();
    return d.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

// 导出全局函数
window.YiJingApp = {
    showNotification,
    copyToClipboard,
    formatDateTime
};

console.log('易镜JavaScript模块加载完成');