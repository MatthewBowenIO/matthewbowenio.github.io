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
  return new Promise(async (resolve, reject) => {
    try {
      const response = await fetch('json/digimon.json');
      cards = await response.json();  // Assign the loaded cards locally
      cards = cards.filter(card => {
        return card.customAttributes.cardType?.length > 0;
      });

      // Resolve the promise with the loaded cards
      resolve(cards);
    } catch (error) {
      // Reject the promise with the error
      reject(error);
    }
  });
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
  return new Promise((resolve) => {
    try {
      const filteredCards = cards.filter(card => {
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

      // Resolve the Promise with the filtered cards
      resolve(filteredCards);
    } catch (error) {
      console.error('Error in searchCards function:', error);
      // Resolve the Promise with an empty array in case of an error
      resolve([]);
    }
  });
}

function search() {
  console.log(document.getElementById('color'));
  const searchParams = {
    "text_all": [document.getElementById("text").value],
    "customAttributes.description": cardAbilities,
    "customAttributes.inheritedEffect": inheritedAbilities,
    "customAttributes.color": color,
    "customAttributes.levelLv": level,
  };

  console.log(searchParams);

  const resultsContainer = document.getElementById('resultsContainer');
  resultsContainer.innerHTML = '';

  // Wrap the asynchronous operation in a Promise
  return new Promise((resolve, reject) => {
    try {
      // Assuming searchCards is an asynchronous function that returns a Promise
      searchCards(searchParams)
        .then(results => {
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
            valueElement.innerHTML = USDollar.format(card.lowestPrice);

            cardElement.appendChild(valueElement);

            resultsContainer.appendChild(cardElement);
          });

          // Resolve the Promise with the results
          resolve(results);
        })
        .catch(error => {
          console.error('Error searching cards:', error);
          reject(error); // Reject the Promise if there's an error
        });
    } catch (error) {
      console.error('Error in search function:', error);
      reject(error); // Reject the Promise if there's an error
    }
  });
}

function buttonSort() {
  sort().then(() => {
    search();
    console.log("Sorted");
  });
}

function sort() {
  return new Promise((resolve, reject) => {
    try {
      cards.sort((a, b) => {
        const getValue = (obj, prop) => {
          const rootValue = obj[prop];
          const customAttributeValue = obj.customAttributes[prop];

          return rootValue !== undefined ? rootValue : (customAttributeValue !== undefined ? customAttributeValue : Number.MAX_VALUE);
        };

        if (sortDirection === 'asc') {
          return getValue(a, sortBy) - getValue(b, sortBy);
        } else if (sortDirection === 'desc') {
          return getValue(b, sortBy) - getValue(a, sortBy);
        }
      });

      // Resolve the Promise with the sorted cards
      resolve(cards);
    } catch (error) {
      console.error('Error in sort function:', error);
      // Reject the Promise if there's an error
      reject(error);
    }
  });
}

function getCheapestPrintings(products) {
  const groupedProducts = products.reduce((result, product) => {
    const number = product.customAttributes.number;
    if (!result[number]) {
      result[number] = [];
    }
    result[number].push(product);
    return result;
  }, {});

  const cheapestRecords = Object.values(groupedProducts).map((group) => {
    return group.reduce((cheapest, product) => {
      return product.lowestPrice < cheapest.lowestPrice ? product : cheapest;
    });
  });


  return cheapestRecords;
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

$('#printingVersions').on('change', function(){
    const versions = $('#printingVersions').val();
    if (versions == 'cheapest') {
      cards = getCheapestPrintings(cards);
      sort().then(() => {
        search();
      });
    } else {
      loadCards()
        .then(cards => {
            sort().then(() => {
              console.log("sorted");
              search();
            });
        })
        .catch(error => {
          console.error('Error loading cards:', error);
        });
    }
});