function toggleAccordion(id) {
    const accordionBody = document.getElementById(id);
    accordionBody.style.display = accordionBody.style.display === "block" ? "none" : "block";
}

document.getElementById('expandAll').addEventListener('click', function () {
    document.querySelectorAll('.accordion-button').forEach(button => {
        if (!button.classList.contains('collapsed')) return;
        button.click();
    });
});

document.getElementById('collapseAll').addEventListener('click', function () {
    document.querySelectorAll('.accordion-button').forEach(button => {
        if (button.classList.contains('collapsed')) return;
        button.click();
    });
});

document.getElementById('searchInput').addEventListener('input', function () {
    const query = this.value.toLowerCase();
    const features = document.querySelectorAll('.feature');

    features.forEach(feature => {
        const text = feature.getAttribute('data-search').toLowerCase();
        feature.style.display = text.includes(query) ? '' : 'none';
    });
});

document.querySelectorAll('.accordion-button').forEach(button => {
    button.addEventListener('click', function () {
        const target = button.getAttribute('data-bs-target').replace('#collapse', '');
        const featureDetails = document.getElementById(`featureDetails${target}`);
        if (featureDetails.getAttribute('data-loaded') === 'true') return;

        fetch(`/reading-mode/feature-details/${target}`)
            .then(response => response.json())
            .then(data => {
                featureDetails.innerHTML = `
                    <h5>Intent</h5>
                    <p>${data.intent}</p>
                    <h5>Parts</h5>
                    <ul>${data.parts.map(part => `<li>${part}</li>`).join('')}</ul>
                    <h5>Spaces</h5>
                    <ul>${data.spaces.map(space => `<li>${space}</li>`).join('')}</ul>
                    <h5>Options</h5>
                    <ul>${data.options.map(option => `<li>${option}</li>`).join('')}</ul>
                    <h5>Requirements</h5>
                    <ul>${data.requirements.map(requirement => `<li>${requirement}</li>`).join('')}</ul>
                `;
                featureDetails.setAttribute('data-loaded', 'true');
            })
            .catch(error => {
                featureDetails.innerHTML = `<p>Error loading details.</p>`;
            });
    });
});




