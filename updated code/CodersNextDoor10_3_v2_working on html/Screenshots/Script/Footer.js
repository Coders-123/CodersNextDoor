// Add a click event listener to the footer links
document.querySelectorAll('.footer-content p').forEach(link => {
	link.addEventListener('click', () => {
		alert('This link is not active');
	});
});

// This code adds an onclick event to the envelope element
// that opens the user's default email application
const envelope = document.querySelector(".envelope");
envelope.addEventListener("click", function() {
  window.location.href = "mailto:";
});
