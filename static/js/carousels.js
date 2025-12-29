// Project Carousels
document.addEventListener('DOMContentLoaded', function() {
    const carousels = document.querySelectorAll('.project-carousel');
    
    carousels.forEach(carousel => {
        const track = carousel.querySelector('.carousel-track');
        const prevBtn = carousel.querySelector('.carousel-prev');
        const nextBtn = carousel.querySelector('.carousel-next');
        const cards = carousel.querySelectorAll('.project-card');
        
        if (!track || cards.length === 0) return;
        
        let currentIndex = 0;
        const maxIndex = Math.max(0, cards.length - 1);
        let userHasInteracted = false; // Track if user has interacted with carousel
        
        function updateCarousel() {
            // Use track.scrollTo to only scroll horizontally, preventing page scroll
            const card = cards[currentIndex];
            if (card && track) {
                // Calculate the scroll position to center the card
                const cardRect = card.getBoundingClientRect();
                const trackRect = track.getBoundingClientRect();
                const scrollLeft = track.scrollLeft;
                const cardLeft = cardRect.left - trackRect.left + scrollLeft;
                const cardWidth = cardRect.width;
                const trackWidth = trackRect.width;
                const targetScroll = cardLeft - (trackWidth / 2) + (cardWidth / 2);
                
                // Only scroll the track horizontally, not the page
                track.scrollTo({
                    left: targetScroll,
                    behavior: 'smooth'
                });
            }
            
            // Update button states
            if (prevBtn) prevBtn.style.opacity = currentIndex === 0 ? '0.5' : '1';
            if (nextBtn) nextBtn.style.opacity = currentIndex >= maxIndex ? '0.5' : '1';
        }
        
        // Ensure cards are properly sized to track visible width
        function resizeCards() {
            const trackWidth = track.clientWidth;
            const gap = 32; // 2rem in pixels (approximate, will be calculated)
            cards.forEach(card => {
                // Set card width to exactly match visible track width
                card.style.width = trackWidth + 'px';
                card.style.minWidth = trackWidth + 'px';
                card.style.maxWidth = trackWidth + 'px';
                card.style.flexShrink = '0';
            });
        }
        
        // Resize on load and resize
        resizeCards();
        let resizeTimer;
        window.addEventListener('resize', function() {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => {
                resizeCards();
                // Only update carousel position on resize if user has interacted with it
                // This prevents unwanted page scrolling when window is resized/zoomed
                if (userHasInteracted) {
                    updateCarousel();
                } else {
                    // Just update the index based on current scroll position
                    updateIndexFromScroll();
                }
            }, 100);
        });
        
        // Update index based on scroll position
        function updateIndexFromScroll() {
            const trackRect = track.getBoundingClientRect();
            let closestIndex = 0;
            let closestDistance = Infinity;
            
            cards.forEach((card, index) => {
                const cardRect = card.getBoundingClientRect();
                const cardCenter = cardRect.left + cardRect.width / 2;
                const trackCenter = trackRect.left + trackRect.width / 2;
                const distance = Math.abs(cardCenter - trackCenter);
                
                if (distance < closestDistance) {
                    closestDistance = distance;
                    closestIndex = index;
                }
            });
            
            currentIndex = closestIndex;
            if (prevBtn) prevBtn.style.opacity = currentIndex === 0 ? '0.5' : '1';
            if (nextBtn) nextBtn.style.opacity = currentIndex >= maxIndex ? '0.5' : '1';
        }
        
        // Previous button
        if (prevBtn) {
            prevBtn.addEventListener('click', function() {
                if (currentIndex > 0) {
                    currentIndex--;
                    userHasInteracted = true;
                    updateCarousel();
                }
            });
        }
        
        // Next button
        if (nextBtn) {
            nextBtn.addEventListener('click', function() {
                if (currentIndex < maxIndex) {
                    currentIndex++;
                    userHasInteracted = true;
                    updateCarousel();
                }
            });
        }
        
        // Update index when user scrolls manually
        track.addEventListener('scroll', function() {
            userHasInteracted = true;
            updateIndexFromScroll();
        });
        
        // Initialize - but don't call updateCarousel immediately to avoid page scroll
        // updateCarousel will be called when user interacts with carousel
        // Just set up the initial state
        if (prevBtn) prevBtn.style.opacity = currentIndex === 0 ? '0.5' : '1';
        if (nextBtn) nextBtn.style.opacity = currentIndex >= maxIndex ? '0.5' : '1';
    });
    
    // Handle project card hover effect
    const projectCards = document.querySelectorAll('.project-card');
    projectCards.forEach(card => {
        const summary = card.querySelector('.project-summary');
        if (summary) {
            const originalText = summary.textContent;
            
            card.addEventListener('mouseenter', function() {
                // Text change is handled by CSS
            });
            
            card.addEventListener('mouseleave', function() {
                // Text reverts via CSS
            });
        }
    });
});

