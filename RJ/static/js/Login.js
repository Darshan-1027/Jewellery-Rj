
  function Eyeclick() {
    const eye = document.getElementById("eye");
    const password = document.getElementById("password");

    if (password.type === "password") {
      password.type = "text";
      eye.classList.remove("fa-eye-slash");
      eye.classList.add("fa-eye");
    } else {
      password.type = "password";
      eye.classList.remove("fa-eye");
      eye.classList.add("fa-eye-slash");
    }
  }

