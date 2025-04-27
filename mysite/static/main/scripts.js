document.addEventListener('DOMContentLoaded', function() {
    const loadPostsBtn = document.getElementById('load-posts');
    if (loadPostsBtn) {
        loadPostsBtn.addEventListener('click', function() {
            fetch('/fetch-posts/')
            .then(response => response.json())
            .then(data => {
                const postsDiv = document.getElementById('posts');
                postsDiv.innerHTML = '';
                data.forEach(post => {
                    postsDiv.innerHTML += `
                        <h3>${post.title}</h3>
                        <p>${post.content}</p>
                        <small>By ${post.author__username}</small>
                        <hr>
                    `;
                });
            });
        });
    }
});
