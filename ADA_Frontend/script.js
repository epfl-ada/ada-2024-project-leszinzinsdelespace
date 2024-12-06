document.addEventListener("DOMContentLoaded", () => {
  const sections = document.querySelectorAll(".section");
  const navItems = document.querySelectorAll(".side-nav li");
  const navIndicator = document.querySelector(".nav-indicator::after");

  // Calculate the total height of the navigation
  const calculateIndicatorPosition = (index) => {
    // Get all nav items
    const navItems = document.querySelectorAll(".side-nav li");
    let position = 0;

    // Calculate position based on actual positions of nav items
    for (let i = 0; i < index; i++) {
      position += navItems[i].offsetHeight + 20; // 20px is the gap between items
    }

    return `${position}px`;
  };

  // Update active nav item on scroll
  const updateActiveNav = () => {
    console.log("-------------------------------");
    const scrollPosition = window.scrollY + window.innerHeight / 2; // Use middle of viewport
    console.log("scrollPosition", scrollPosition);

    // Find the current section
    let found = false;
    let currentSectionIndex = 0;
    sections.forEach((section, index) => {
      if (found) {
        console.log("Already found, skipping");
        return;
      }
      const sectionTop = section.getBoundingClientRect().top + window.pageYOffset-20;
      const sectionBottom = section.getBoundingClientRect().bottom + window.pageYOffset-20;
      console.log("section ", section.id,": [", sectionTop, " , ", sectionBottom, "]");

      // Check if scroll position is within section bounds
      if (scrollPosition >= sectionTop && scrollPosition <= sectionBottom) {
        
        found = true;
        console.log(
          "scrollPosition (",
          scrollPosition,
          ") is within section ",
          section.id,
          " : from (",
          sectionTop,
          " to ",
          sectionBottom,
          ")"
        );
        currentSectionIndex = index;

        // Remove active class from all nav items
        navItems.forEach((item) => item.classList.remove("active"));

        // Add active class to current nav item
        navItems[index].classList.add("active");
        console.log("currentSectionIndex", currentSectionIndex);

        // Update indicator position
        document.documentElement.style.setProperty(
          "--nav-indicator-top",
          calculateIndicatorPosition(index)
        );

      }
    });

    // Handle last section specially
    const lastSection = sections[sections.length - 1];
    if (
      window.innerHeight + window.scrollY >=
      document.documentElement.scrollHeight - 100
    ) {
      currentSectionIndex = sections.length - 1;
      navItems.forEach((item) => item.classList.remove("active"));
      navItems[currentSectionIndex].classList.add("active");
      document.documentElement.style.setProperty(
        "--nav-indicator-top",
        calculateIndicatorPosition(currentSectionIndex)
      );
    }
  };

  // Smooth scroll to section when clicking nav items
  navItems.forEach((item) => {
    item.addEventListener("click", (e) => {
      e.preventDefault();
      const targetId = item.querySelector("a").getAttribute("href");
      const targetSection = document.querySelector(targetId);

      window.scrollTo({
        top: targetSection.getBoundingClientRect().top + window.pageYOffset-100,
        behavior: "smooth",
      });
    });
  });

  // Listen for scroll events
  window.addEventListener("scroll", updateActiveNav);

  // Initial update
  updateActiveNav();

  // Function to fetch similarity score from backend
  async function fetchSimilarityScore(startArticle, targetArticle) {
    try {
      const response = await fetch("/api/similarity", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          start: startArticle,
          target: targetArticle,
        }),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      return data.similarityScore;
    } catch (error) {
      console.error("Error fetching similarity score:", error);
      return null;
    }
  }

  // Function to update the UI with the similarity score
  function updateSimilarityScore(score) {
    const similarityValue = document.querySelector(".similarity-value");
    if (similarityValue) {
      // Animate the score change
      const currentScore = parseFloat(similarityValue.dataset.score);
      const newScore = parseFloat(score);

      // Simple animation of the score
      const duration = 1000; // 1 second
      const start = performance.now();

      function updateScore(currentTime) {
        const elapsed = currentTime - start;
        const progress = Math.min(elapsed / duration, 1);

        const currentValue =
          currentScore + (newScore - currentScore) * progress;
        similarityValue.textContent = currentValue.toFixed(2);

        if (progress < 1) {
          requestAnimationFrame(updateScore);
        } else {
          similarityValue.dataset.score = newScore;
        }
      }

      requestAnimationFrame(updateScore);
    }
  }

  // Event listener for the GO button
  document.querySelector(".go-button")?.addEventListener("click", async () => {
    const startInput = document.querySelector(
      'input[placeholder="start article"]'
    );
    const targetInput = document.querySelector(
      'input[placeholder="target article"]'
    );

    if (startInput && targetInput) {
      const startArticle = startInput.value.trim();
      const targetArticle = targetInput.value.trim();

      if (startArticle && targetArticle) {
        // For now, use the hardcoded value
        updateSimilarityScore(0.87);

        // When backend is ready, uncomment this:
        // const score = await fetchSimilarityScore(startArticle, targetArticle);
        // if (score !== null) {
        //     updateSimilarityScore(score);
        // }
      }
    }
  });

  // Add mobile nav synchronization
  if (window.innerWidth <= 768) {
    const updateMobileNav = () => {
      const activeNavItem = document.querySelector(".side-nav li.active");
      if (activeNavItem) {
        // Calculate scroll position
        const navList = document.querySelector(".side-nav ul");
        const itemLeft = activeNavItem.offsetLeft;
        const navWidth = navList.offsetWidth;
        const itemWidth = activeNavItem.offsetWidth;

        // Calculate the ideal scroll position to center the item
        const scrollLeft = itemLeft - navWidth / 2 + itemWidth / 2;

        // Smooth scroll to the position
        navList.scrollTo({
          left: scrollLeft,
          behavior: "smooth",
        });
      }
    };

    // Update nav scroll position when active item changes
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (
          mutation.type === "attributes" &&
          mutation.attributeName === "class"
        ) {
          updateMobileNav();
        }
      });
    });

    // Observe all nav items for class changes
    document.querySelectorAll(".side-nav li").forEach((item) => {
      observer.observe(item, {
        attributes: true,
        attributeFilter: ["class"],
      });
    });

    // Initial update
    updateMobileNav();

    // Update on scroll
    window.addEventListener("scroll", updateMobileNav);
  }
});
