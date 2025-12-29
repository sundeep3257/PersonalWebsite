// Experience Flip Cards
document.addEventListener('DOMContentLoaded', function() {
    const experienceCards = document.querySelectorAll('.experience-card');
    
    experienceCards.forEach(card => {
        // Ensure proper 3D transform
        const inner = card.querySelector('.experience-card-inner');
        if (!inner) return;
        
        // Add smooth transition
        inner.style.transition = 'transform 0.6s';
        inner.style.transformStyle = 'preserve-3d';
        
        // Ensure both sides are properly positioned
        const front = card.querySelector('.experience-front');
        const back = card.querySelector('.experience-back');
        
        if (front && back) {
            front.style.backfaceVisibility = 'hidden';
            back.style.backfaceVisibility = 'hidden';
            back.style.transform = 'rotateY(180deg)';
        }
        
        // Touch support for mobile
        let touchStartX = 0;
        let touchEndX = 0;
        
        card.addEventListener('touchstart', function(e) {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });
        
        card.addEventListener('touchend', function(e) {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        }, { passive: true });
        
        function handleSwipe() {
            const swipeThreshold = 50;
            const diff = touchStartX - touchEndX;
            
            if (Math.abs(diff) > swipeThreshold) {
                if (diff > 0) {
                    // Swipe left - flip
                    inner.style.transform = 'rotateY(180deg)';
                } else {
                    // Swipe right - unflip
                    inner.style.transform = 'rotateY(0deg)';
                }
            }
        }
    });
});

