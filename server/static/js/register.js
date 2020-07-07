function checkPassword(form) {
    password1 = form.Password.value;
    password2 = form.Password1.value;

    // If password not entered
    if (password1 === '') {
        alert("Please enter Password");
        return false
    }
    // If confirm password not entered
    else if (password2 === '') {
        alert("Please enter confirm password");
        return false
    }

    // If Not same return False.
    else if (password1 != password2) {
        alert ("\nPassword did not match: Please try again...")
        return false
    }

    // If same return True.
    else{
        alert("Passwords Match")
        return true
    }
  }



