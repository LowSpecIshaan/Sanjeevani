// Tab switching logic
const loginTab = document.getElementById('login-tab');
const signupTab = document.getElementById('signup-tab');
const loginPanel = document.getElementById('login-panel');
const signupPanel = document.getElementById('signup-panel');

function switchTab(selectedTab) {
  if (selectedTab === 'login') {
    loginTab.classList.add('active');
    signupTab.classList.remove('active');

    loginPanel.classList.remove("hidden");
    signupPanel.classList.add("hidden");
  } else {
    signupTab.classList.add('active');
    loginTab.classList.remove('active');

    signupPanel.classList.remove("hidden");
    loginPanel.classList.add("hidden");
  }
}

loginTab.addEventListener('click', () => switchTab('login'));
signupTab.addEventListener('click', () => switchTab('signup'));

// Keyboard accessibility for tabs
[loginTab, signupTab].forEach((tab) => {
  tab.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
      e.preventDefault();
      if (tab === loginTab) {
        switchTab('signup');
        signupTab.focus();
      } else {
        switchTab('login');
        loginTab.focus();
      }
    }
  });
});


// Login form: toggle email / aadhaar input fields
const loginMethodRadios = document.querySelectorAll(
  'input[name="loginMethod"]'
);
const emailField = document.getElementById('emailField');
const aadhaarField = document.getElementById('aadhaarField');

function updateLoginFields() {
  const selectedMethod = document.querySelector(
    'input[name="loginMethod"]:checked'
  ).value;
  if (selectedMethod === 'email') {
    emailField.classList.remove('hidden');
    emailField.querySelector('input').setAttribute('required', 'required');
    aadhaarField.classList.add('hidden');
    aadhaarField.querySelector('input').removeAttribute('required');
  } else {
    aadhaarField.classList.remove('hidden');
    aadhaarField.querySelector('input').setAttribute('required', 'required');
    emailField.classList.add('hidden');
    emailField.querySelector('input').removeAttribute('required');
  }
}

loginMethodRadios.forEach((radio) =>
  radio.addEventListener('change', updateLoginFields)
);

updateLoginFields(); // initialize on page load

// Login form validation and submission
document.getElementById('loginForm').addEventListener('submit', (e) => {
  const selectedMethod = document.querySelector(
    'input[name="loginMethod"]:checked'
  ).value;
  let valid = true;
  let errorMsg = '';

  if (selectedMethod === 'email') {
    const email = document.getElementById('email').value.trim();
    if (!email) {
      valid = false;
      errorMsg = 'Please enter your Email ID.';
    }
  } else {
    const aadhaar = document.getElementById('aadhaar').value.trim();
    if (!aadhaar || aadhaar.length !== 12 || !/^\d{12}$/.test(aadhaar)) {
      valid = false;
      errorMsg = 'Please enter a valid 12-digit Aadhaar Card Number.';
    }
  }

  const password = document.getElementById('password').value;
  if (!password) {
    valid = false;
    errorMsg = (errorMsg ? errorMsg + ' ' : '') + 'Please enter your password.';
  }

  if (!valid) {
    alert(errorMsg);
    return;
  }

  // Simulate login (in real app, send to server with checked radio for method)
});

// Signup form validation and submission
document.getElementById('signupForm').addEventListener('submit', (e) => {
  let valid = true;
  let errorMsg = '';

  const name = document.getElementById('signupName').value.trim();
  if (!name) {
    valid = false;
    errorMsg += 'Please enter your full name. ';
  }

  const aadhaar = document.getElementById('signupAadhaar').value.trim();
  if (!aadhaar || aadhaar.length !== 12 || !/^\d{12}$/.test(aadhaar)) {
    valid = false;
    errorMsg += 'Please enter a valid 12-digit Aadhaar Card Number. ';
  }

  const email = document.getElementById('signupEmail').value.trim();
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!email || !emailPattern.test(email)) {
    valid = false;
    errorMsg += 'Please enter a valid Email ID. ';
  }

  const password = document.getElementById('signupPassword').value;
  const confirmPassword = document.getElementById('signupPasswordConfirm').value;
  if (!password || password.length < 6) {
    valid = false;
    errorMsg += 'Please create a password with at least 6 characters. ';
  } else if (password !== confirmPassword) {
    valid = false;
    errorMsg += 'Passwords do not match. ';
  }

  const termsCheckbox = document.getElementById('tandc');
  if (!termsCheckbox.checked) {
    valid = false;
    errorMsg += 'You must agree to the Terms & Conditions. ';
  }

  if (!valid) {
    e.preventDefault(); // ❌ only stop submission if invalid
    alert(errorMsg);
  }
});



// Simple input validation for Aadhaar fields to allow only digits
const aadhaarInputs = document.querySelectorAll('input[name="aadhaar"]');
aadhaarInputs.forEach(input => {
  input.addEventListener('input', function() {
    this.value = this.value.replace(/\D/g, '');
  });
});