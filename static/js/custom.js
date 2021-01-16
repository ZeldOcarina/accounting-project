// Helpers
function setFormSelects(customerSelect, vendorSelect) {
    if(kindSelect.value === 'Expense') {
        customerSelect.parentElement.classList.add("hidden")
        vendorSelect.parentElement.classList.remove("hidden")
    } else {
        customerSelect.parentElement.classList.remove("hidden")
        vendorSelect.parentElement.classList.add("hidden")
    }
}

function queryOrganizer(queries) {
    return queries
      .replace("?", "")
      .split("&")
      .reduce(function (acc, query) {
        return [...acc, { [query.split("=")[0]]: query.split("=")[1] }];
    }, []);
}

// Form helper
if (window.location.pathname === '/line-items/create') {
    form = document.querySelector('form')
    kindSelect = document.getElementById("kind")
    customerSelect = document.getElementById("customer")
    vendorSelect = document.getElementById("vendor")

    setFormSelects(customerSelect, vendorSelect)
    kindSelect.addEventListener("change", function() {
        setFormSelects(customerSelect, vendorSelect)
    })
}

// Delete request
if (window.location.pathname === '/') {
    deleteIcons = Array.from(document.getElementsByClassName("delete-icon"));
    deleteIcons.forEach(function(icon) {
        icon.addEventListener("click", function(e) {
            if(!confirm("Vuoi cancellare la transazione? L'operazione è irreversibile.")) return
            fetch(`/line-items/${icon.dataset.itemId}`, {
                method: "DELETE",
            }).then(function(response) {
                history.go()
            }).catch(function(err) {
                console.dir(err)
            })
        })
    })
}

// Flash animation
if (document.querySelector(".flash-message")) {
    const flashMessage = document.querySelector('.flash-message');
    setTimeout(function() {
        flashMessage.style.opacity = 0;
    }, 3000)
}

// Daterange
let startDate, endDate;
if(window.location.search) {
    const query = queryOrganizer(window.location.search);
    const daterangeQuery = query.find((item) => item.daterange)
    const fromDateString = daterangeQuery.daterange.split("-")[0].replace('+', '').replaceAll('2F', '').replaceAll('%', '/')
    const endDateString = daterangeQuery.daterange.split("-")[1].replace('+', '').replaceAll('2F', '').replaceAll('%', '/')
    startDate = moment(fromDateString, 'DD/MM/YYYY').toDate();
    endDate = moment(endDateString, 'DD/MM/YYYY').toDate();
}

$('input[name="daterange"]').daterangepicker({
    "startDate": startDate ? startDate : moment().subtract(30, 'days'),
    "endDate": endDate ? endDate : moment(),
    "locale": {
        "format": "DD/MM/YYYY",
        "separator": " - "
    },
    "ranges": {
        'Last 7 Days': [moment().subtract(6, 'days'), moment()],
        'Last 30 Days': [moment().subtract(29, 'days'), moment()],
        'This Month': [moment().startOf('month'), moment().endOf('month')],
        'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
    }
});

// Set footer date
const dateSpan = document.querySelector('.date');
dateSpan.textContent = new Date().getFullYear();