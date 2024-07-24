document.addEventListener("DOMContentLoaded", function () {
  // Use like and unlike buttons on posts
  document.querySelectorAll("#like").forEach((likeButton) => {
    likeButton.onclick = function () {
      const post_id = likeButton.dataset.id;
      const like = likeButton.ariaLabel.toLowerCase() === "like" ? true : false;
      console.log(
        `Clicked ${likeButton.ariaLabel.toLowerCase()} for post ${post_id}`
      );

      // Like or Unlike the post
      fetch(`/post/${post_id}`, {
        method: "PUT",
        body: JSON.stringify({
          like: like,
        }),
      });
    };
  });
});
