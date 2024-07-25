document.addEventListener("DOMContentLoaded", function () {
  // Use like and unlike buttons on posts
  document.querySelectorAll("#like").forEach((likeButton) => {
    likeButton.onclick = function () {
      const postId = likeButton.dataset.id;
      const like = likeButton.ariaLabel.toLowerCase() === "like" ? true : false;

      // Like or Unlike the post
      fetch(`/post/${postId}`, {
        method: "PUT",
        body: JSON.stringify({
          like: like,
        }),
      }).then((res) => {
        // Check for unsuccessful update
        if (res.status !== 204) {
          console.error(`Error: ${res}`);
        }

        // Update like/unlike button and like count
        updateLike(likeButton);
      });
    };
  });
});

function updateLike(likeButton) {
  const postId = likeButton.dataset.id;
  const currentUser = document.querySelector("#current-user").innerHTML.trim();

  // Get current state of the post
  fetch(`/post/${postId}`)
    .then((res) => res.json())
    .then((post) => {
      const likeCountSpan = likeButton.nextElementSibling;

      // Update like or unlike button
      if (post.liked.includes(currentUser)) {
        likeButton.ariaLabel = "Unlike";
        likeButton.innerHTML = `<i class="bi bi-heart-fill text-danger"></i>`;
      } else {
        likeButton.ariaLabel = "Like";
        likeButton.innerHTML = `<i class="bi bi-heart text-danger"></i>`;
      }

      // Update like count
      likeButton.nextElementSibling.innerText = post.liked.length;
    });
}
