$.validator.addMethod("lettersonly", function (value, element) {
    return this.optional(element) || /^[A-Za-zА-Яа-яЁё]+$/i.test(value);
}, "Letters only please");

$.validator.addMethod("passwordValidation", function (value, element) {
    return this.optional(element) || /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{4,}$/i.test(value);
}, "Password invalid format");

$.validator.addMethod("emailValidation", function (value, element) {
    return this.optional(element) || /^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i.test(value);
}, "Please enter a valid email address.");

$("#sign-up-form").validate({
    rules: {
        password: {
            required: true,
            minlength: 4,
            passwordValidation: true
        },
        confirm_password: {
            required: true,
            equalTo: "#RegisterFormPassword",
            minlength: 4,
            passwordValidation: true
        },
        email: {
            required: true,
            emailValidation:true
        },
        first_name: {
            required: true,
            lettersonly: true
        },
        last_name: {
            required: true,
            lettersonly: true

        }
    },
    messages: {
        password: {
            required: "Please enter a password",
            minlength: "Your password must be at least 8 characters long"
        },
        confirm_password: {
            required: "Please repeat the password",
            equalTo: "This password doesn't match with the original password",
            minlength: "Your password must be at least 8 characters long"
        },
        email: {
            required: "Please enter a email"
        },
        first_name: {
            required: "Please enter a name"

        },
        last_name: {
            required: "Please enter a surname"

        }
    }
});