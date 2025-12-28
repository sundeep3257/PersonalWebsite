// Falling snow effect for homepage
(function() {
    'use strict';
    
    // Only run on homepage
    if (!document.body.classList.contains('homepage')) {
        return;
    }
    
    // Wait for DOM to be ready
    document.addEventListener('DOMContentLoaded', function() {
        // Find the skills section to start snow from there
        const skillsSection = document.getElementById('skills');
        if (!skillsSection) {
            return;
        }
        
        // Create snow container
        const snowContainer = document.createElement('div');
        snowContainer.className = 'snow-container';
        document.body.appendChild(snowContainer);
        
        // Number of snowflakes
        const snowflakeCount = 15;
        
        // Get skills section position
        function getSkillsTop() {
            return skillsSection.getBoundingClientRect().top + window.pageYOffset;
        }
        
        // Create snowflakes
        function createSnowflake() {
            const snowflake = document.createElement('div');
            snowflake.className = 'snowflake';
            
            // Random size between 4px and 10px
            const size = Math.random() * 6 + 4;
            snowflake.style.width = size + 'px';
            snowflake.style.height = size + 'px';
            
            // Random horizontal position
            snowflake.style.left = Math.random() * 100 + '%';
            
            // Random animation duration (falling speed) between 8s and 18s
            const duration = Math.random() * 10 + 8;
            snowflake.style.animationDuration = duration + 's';
            
            // Random delay to stagger the snowflakes
            snowflake.style.animationDelay = Math.random() * 3 + 's';
            
            // Start from the top of the skills section (relative to viewport)
            const skillsTop = skillsSection.getBoundingClientRect().top;
            // Only create snowflake if skills section is visible or above viewport
            if (skillsTop <= window.innerHeight) {
                snowflake.style.top = Math.max(0, skillsTop) + 'px';
                snowContainer.appendChild(snowflake);
                
                // Remove snowflake after animation completes
                setTimeout(() => {
                    if (snowflake.parentNode) {
                        snowflake.parentNode.removeChild(snowflake);
                    }
                }, (duration + 3) * 1000);
            }
        }
        
        // Create initial snowflakes
        for (let i = 0; i < snowflakeCount; i++) {
            setTimeout(() => {
                createSnowflake();
            }, i * 150); // Stagger creation
        }
        
        // Continuously create new snowflakes
        setInterval(() => {
            createSnowflake();
        }, 1200);
    });
})();

