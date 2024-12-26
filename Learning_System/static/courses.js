    // Get all accordion buttons
    const accordionBtns = document.querySelectorAll('.accordion-btn');

    accordionBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Toggle the active class for the current item
            const parent = btn.parentElement;
            parent.classList.toggle('active');
    
            // Close other open accordions
            document.querySelectorAll('.accordion-item').forEach(item => {
                if (item !== parent) {
                    item.classList.remove('active');
                }
            });
        });
    });