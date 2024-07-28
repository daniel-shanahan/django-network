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

  // Edit buttons on a user's own posts
  document.querySelectorAll("#edit").forEach((editButton) => {
    editButton.onclick = function () {
      editPost(editButton);
    };
  });
});

function editPost(editButton) {
  // Hide edit button while editing
  editButton.classList.toggle("d-none");

  const postId = editButton.dataset.id;

  // Get the current body element
  const bodyElement = editButton.parentElement.nextElementSibling;

  // Create elements for editing/saving new post body
  const divElement = document.createElement("div");
  const textareaDivElement = document.createElement("div");
  const editBodyElement = document.createElement("textarea");
  const saveButton = document.createElement("button");

  divElement.className = "mb-2";

  textareaDivElement.className = "form-group";

  editBodyElement.id = "edit-post";
  editBodyElement.name = "edit-post";
  editBodyElement.rows = "2";
  editBodyElement.className = "form-control";
  editBodyElement.innerText = bodyElement.innerText;

  saveButton.type = "submit";
  saveButton.className = "btn btn-primary d-block";
  saveButton.innerText = "Save";
  saveButton.onclick = function () {
    // Update the post body
    fetch(`/post/${postId}`, {
      method: "PUT",
      body: JSON.stringify({
        body: editBodyElement.value,
      }),
    }).then(() => {
      // Get updated post
      fetch(`/post/${postId}`)
        .then((res) => res.json())
        .then((post) => {
          // Display updated post
          bodyElement.innerText = post.body;
          divElement.replaceWith(bodyElement);

          // Show edit button
          editButton.classList.toggle("d-none");
        });
    });
  };

  // Insert editing elements in place of the current body
  textareaDivElement.appendChild(editBodyElement);
  divElement.appendChild(textareaDivElement);
  divElement.appendChild(saveButton);
  bodyElement.replaceWith(divElement);
}

function updateLike(likeButton) {
  const postId = likeButton.dataset.id;
  const currentUser = document.querySelector("#current-user").innerHTML.trim();

  // Get current state of the post
  fetch(`/post/${postId}`)
    .then((res) => res.json())
    .then((post) => {
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
