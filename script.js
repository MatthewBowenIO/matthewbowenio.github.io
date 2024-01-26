let cards = [];  // Declare cards globally
let cardAbilities = [];
let inheritedAbilities = [];
let color = [];
let level = [];
let sortDirection = '';
let sortBy = '';

let USDollar = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
});

async function loadCards() {
  try {
    const response = await fetch('json/digimon.json');
    cards = await response.json();  // Assign the loaded cards globally
    cards = cards.filter(card => {
      return card.customAttributes.cardType?.length > 0;
    });
  } catch (error) {
    console.error('Error loading cards:', error);
    cards = [];
  }
}

function generateListItems(listId, data) {
  const list = $(`#${listId}`);

  // Clear existing content
  list.empty();

  // Use jQuery each to iterate over the data array and generate list items
  $.each(data, function(index, value) {
    const listItem = $('<option>').text(value.value).value(value.value);
    list.append(listItem);
  });
}

function searchCards(searchParams) {
  return cards.filter(card => {
    const setNameMatch = !searchParams.setName || card.setName.toLowerCase().includes(searchParams.setName.toLowerCase());
    const productNameMatch = !searchParams.productName || card.productName.toLowerCase().includes(searchParams.productName.toLowerCase());
    const rarityNameMatch = !searchParams.rarityName || card.rarityName.toLowerCase() === searchParams.rarityName.toLowerCase();

    const customAttributesMatch = Object.keys(searchParams).every(key => {
      return searchParams[key].every(searchValue => {
        if (key == 'text_all') {
          if (JSON.stringify(card).toLowerCase().includes(searchParams[key][0].toLowerCase())) {
            return true;
          }
        }

        if (key.startsWith("customAttributes.")) {
          const attributeKey = key.split(".")[1];
          if (card.customAttributes[attributeKey]) {
            if (searchParams[key] == 'null') {
              return true;
            }

            if (Array.isArray(card.customAttributes[attributeKey])) {
              console.log("Is array");
              const combinedValue = card.customAttributes[attributeKey].join(',');
              return combinedValue.toLowerCase().includes(searchValue.toLowerCase());
            }

            return card.customAttributes[attributeKey] && card.customAttributes[attributeKey].toLowerCase().includes(searchValue.toLowerCase());
          }
        }
      });
    });

    return setNameMatch && productNameMatch && rarityNameMatch && customAttributesMatch;
  });
}

function search() {
  console.log(document.getElementById('color'));
  const searchParams = {
    "text_all": [document.getElementById("text").value],
    "customAttributes.description":  cardAbilities,
    "customAttributes.inheritedEffect": inheritedAbilities,
    "customAttributes.color": color,
    "customAttributes.levelLv": level,
  };


  console.log(searchParams);

  const resultsContainer = document.getElementById('resultsContainer');
  resultsContainer.innerHTML = '';

  const results = searchCards(searchParams);

  console.log(results);
  results.forEach(card => {
    const cardElement = document.createElement('div');
    cardElement.classList.add('card');

    const imageSrc = `images/${card.productId}.jpg`;
    const imageElement = document.createElement('img');
    imageElement.src = imageSrc;

    imageElement.setAttribute('data-product-id', card.productId);

    imageElement.addEventListener('click', event => {
      window.open(`https://www.tcgplayer.com/product/${event.target.dataset.productId}?utm_campaign=affiliate&utm_medium=5176242&utm_source=5176242`, "_blank");
    });

    cardElement.appendChild(imageElement);

    const valueElement = document.createElement('label');
    valueElement.innerHTML = USDollar.format(card.lowestPriceWithShipping);

    cardElement.appendChild(valueElement);

    resultsContainer.appendChild(cardElement);
  });
}

function sort() {
  cards.sort((a, b) => {
    if (sortDirection == 'asc') {
      if (sortBy == 'price') {
        return a.lowestPriceWithShipping - b.lowestPriceWithShipping;
      } else if (sortBy == 'play_cost') {
        return a.customAttributes.playCost - b.customAttributes.playcost;
      } else if (sortBy == 'digivolution_cost') {
        return a.customAttributes.digivolve1Cost - b.customAttributes.digivolve1Cost;
      }
    }
    else if (sortDirection == 'desc') {
      if (sortBy == 'price') {
        return b.lowestPriceWithShipping - a.lowestPriceWithShipping;
      } else if (sortBy == 'play_cost') {
        return b.customAttributes.playCost - a.customAttributes.playcost;
      } else if (sortBy == 'digivolution_cost') {
        return b.customAttributes.digivolve1Cost - a.customAttributes.digivolve1Cost;
      }
    }
});

  search();
}

function clearFilters() {
  const resultsContainer = document.getElementById('resultsContainer');
  resultsContainer.innerHTML = '';
   cardAbilities = [];
 inheritedAbilities = [];
 color = [];
 level = [];
 sortDirection = '';
 sortBy = '';
 $('#cardAbilities').val([]);
 $('#inheritedAbilities').val([]);
 $('#color').val([]);
 $('#levelLv').val([]);
  $("#levelLv").prop('selectedIndex', 2);
 $('#sortDirection').val([]);
 $('#sortBy').val([]);
}

 loadCards();
 //loadSearchOptions();

$(function () {
  $('.selectedpicker').selectpicker();
});


$('#cardAbilities').on('change', function(){
    cardAbilities = [...$('#cardAbilities').val()];
});

$('#inheritedAbilities').on('change', function(){
    inheritedAbilities = [...$('#inheritedAbilities').val()];
});

$('#color').on('change', function(){
    color = [...$('#color').val()]
});

$('#levelLv').on('change', function(){
    level = [...$('#levelLv').val()]
});

$('#sortDirection').on('change', function(){
    sortDirection = $('#sortDirection').val();
});

$('#sortBy').on('change', function(){
    sortBy = $('#sortBy').val();
});