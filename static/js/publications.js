// Publications Scroll-Snap Viewer
document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('.publications-container');
    if (!container) return;
    
    const cards = container.querySelectorAll('.publication-card');
    if (cards.length === 0) return;
    
    let currentIndex = 0;
    
    // Set first card as active
    cards[0].classList.add('active');
    
    // Update active card based on scroll position
    function updateActiveCard() {
        const containerRect = container.getBoundingClientRect();
        const containerCenter = containerRect.left + containerRect.width / 2;
        
        let closestCard = null;
        let closestDistance = Infinity;
        
        cards.forEach((card, index) => {
            const cardRect = card.getBoundingClientRect();
            const cardCenter = cardRect.left + cardRect.width / 2;
            const distance = Math.abs(cardCenter - containerCenter);
            
            if (distance < closestDistance) {
                closestDistance = distance;
                closestCard = card;
                currentIndex = index;
            }
        });
        
        // Update active state
        cards.forEach(card => card.classList.remove('active'));
        if (closestCard) {
            closestCard.classList.add('active');
        }
    }
    
    // Scroll event listener
    container.addEventListener('scroll', updateActiveCard);
    
    // Navigation buttons
    const prevBtn = document.querySelector('.pub-prev');
    const nextBtn = document.querySelector('.pub-next');
    
    function scrollToCard(index) {
        if (index < 0 || index >= cards.length) return;
        
        const card = cards[index];
        const containerRect = container.getBoundingClientRect();
        const cardRect = card.getBoundingClientRect();
        const scrollLeft = container.scrollLeft;
        const cardLeft = cardRect.left - containerRect.left + scrollLeft;
        const cardWidth = cardRect.width;
        const containerWidth = containerRect.width;
        const targetScroll = cardLeft - (containerWidth / 2) + (cardWidth / 2);
        
        container.scrollTo({
            left: targetScroll,
            behavior: 'smooth'
        });
        
        currentIndex = index;
    }
    
    if (prevBtn) {
        prevBtn.addEventListener('click', function() {
            if (currentIndex > 0) {
                scrollToCard(currentIndex - 1);
            }
        });
    }
    
    if (nextBtn) {
        nextBtn.addEventListener('click', function() {
            if (currentIndex < cards.length - 1) {
                scrollToCard(currentIndex + 1);
            }
        });
    }
    
    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
        
        if (e.key === 'ArrowLeft' && currentIndex > 0) {
            scrollToCard(currentIndex - 1);
        } else if (e.key === 'ArrowRight' && currentIndex < cards.length - 1) {
            scrollToCard(currentIndex + 1);
        }
    });
    
    // Wheel event for smooth scrolling between cards
    let wheelTimeout;
    container.addEventListener('wheel', function(e) {
        e.preventDefault();
        
        clearTimeout(wheelTimeout);
        wheelTimeout = setTimeout(() => {
            if (e.deltaY > 0 && currentIndex < cards.length - 1) {
                scrollToCard(currentIndex + 1);
            } else if (e.deltaY < 0 && currentIndex > 0) {
                scrollToCard(currentIndex - 1);
            }
        }, 100);
    }, { passive: false });
    
    // Initial update
    updateActiveCard();
    
    // Update on resize
    window.addEventListener('resize', function() {
        setTimeout(updateActiveCard, 100);
    });
});

