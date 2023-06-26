// script.js
const searchInput = document.getElementById('searchInput');
const searchResults = document.getElementById('searchResults');
const loadMoreButton = document.getElementById('loadMoreButton');
let currentQuery = '';
let currentOffset = 0;
let timeout = null;
searchInput.addEventListener('input', () => {
  currentQuery = searchInput.value.trim();
  // console.log(currentQuery);
  if (currentQuery === '') {
    loadMoreButton.hidden = true;
    clearResults();
    return;
  }
  currentOffset = 0;
  clearResults();
  if (timeout) clearTimeout(timeout);

  timeout =  setTimeout(() => {
    searchCars();
  }, 500);
  // searchCars();

});
loadMoreButton.addEventListener('click', loadMore);

function loadMore() {
  currentOffset += 1;
  searchCars();
}

function searchCars() {
  fetch(`/search?q=${encodeURIComponent(currentQuery)}&page=${currentOffset}`)
    .then(response => response.json())
    .then(data => displayResults(data))
    .catch(error => console.error(error));
}
function displayResults(results) {
  loadMoreButton.hidden = false;


  // clearResults();

  if (results.length === 0) {
    clearResults()
    const noResultsItem = document.createElement('li');
    noResultsItem.textContent = 'No results found.';
    searchResults.appendChild(noResultsItem);
    return;
  }

  results.forEach(result => {
    const item = document.createElement('li');
    // item.textContent = JSON.stringify(result);
    // item.appendChild(createCarLi(result));
    searchResults.appendChild(createCarLi(result));
  });
}

function createCarLi(car) {
  const li = document.createElement('li');
  li.style.backgroundColor = '#f2f2f2';
  li.style.padding = '20px';
  li.style.borderRadius = '10px';
  li.style.boxShadow = '0 2px 5px rgba(0, 0, 0, 0.1)';
  // li.style.marginBottom = '20px';

  const h2 = document.createElement('h2');
  h2.style.marginBottom = '10px';
  h2.textContent = `${car.Make} ${car.Model}`;
  li.appendChild(h2);

  const propBox = document.createElement('div');
  propBox.style.display = 'flex';
  propBox.style.gap = '20px';
  propBox.style.flexWrap = 'wrap';
  const keys = ['Price', 'Year', 'Color', 'Location']
  for (const key of keys) {
    if (key !== 'Make' && key !== 'Model') {
      const p = document.createElement('p');
      const strong = document.createElement('strong');
      strong.textContent = `${key}: `;
      p.appendChild(strong);
      p.innerHTML += car[key];
      propBox.appendChild(p);
    }
  }

  li.appendChild(propBox)

  return li;
}


function clearResults() {
  while (searchResults.firstChild) {
    searchResults.removeChild(searchResults.firstChild);
  }
}
