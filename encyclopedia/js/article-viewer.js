/**
 * Переключатель режимов просмотра статей
 * Используется на всех страницах статей, преамбулы и введения
 */

function toggleView() {
    const structuredView = document.querySelector('.article-text');
    const originalView = document.getElementById('originalText');
    const button = document.getElementById('toggleView');

    if (!structuredView || !originalView || !button) {
        console.error('Не найдены необходимые элементы для переключения режимов');
        return;
    }

    if (originalView.style.display === 'none' || originalView.style.display === '') {
        // Показать оригинал
        structuredView.style.display = 'none';
        originalView.style.display = 'block';
        button.textContent = '📖 Показать структурированный вид';
        button.classList.add('active');

        // Сохранить состояние в localStorage
        localStorage.setItem('viewMode', 'original');
    } else {
        // Показать структурированный вид
        structuredView.style.display = 'block';
        originalView.style.display = 'none';
        button.textContent = '📄 Показать оригинальный текст';
        button.classList.remove('active');

        // Сохранить состояние в localStorage
        localStorage.setItem('viewMode', 'structured');
    }
}

// Восстановление режима просмотра при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    const savedMode = localStorage.getItem('viewMode');

    if (savedMode === 'original') {
        // Если пользователь предпочитает оригинальный текст
        const structuredView = document.querySelector('.article-text');
        const originalView = document.getElementById('originalText');
        const button = document.getElementById('toggleView');

        if (structuredView && originalView && button) {
            structuredView.style.display = 'none';
            originalView.style.display = 'block';
            button.textContent = '📖 Показать структурированный вид';
            button.classList.add('active');
        }
    }
});

// Горячие клавиши для переключения режимов
document.addEventListener('keydown', function(event) {
    // Ctrl+Shift+V для переключения режимов
    if (event.ctrlKey && event.shiftKey && event.key === 'V') {
        event.preventDefault();
        toggleView();
    }
});