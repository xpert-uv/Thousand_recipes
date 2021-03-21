BASE_API = "http://localhost:5000";

$("#winebox").hide();
$("#noWine").hide();

$(".card-body").on("click", "#wine-btn", paringWine);

function generateWineHTML_tabs(wine) {

    return ` <li class="nav-item" role="presentation">
            <button class="nav-link" id="${wine}-tab" data-bs-toggle="tab" data-bs-target="#${wine}" type="button"
                role="tab" aria-controls="${wine}" aria-selected="true" data-name="${wine}">${wine}</button>
        </li>`;

}

function generateWineHTML_tab_pannel(wine) {
    return `
         <div class="tab-pane fade" id="${wine}" role="tabpanel" aria-labelledby="${wine}-tab">...</div>
        `;
}

function generateWineHTML_errors(wine) {
    return `<h1 class="display-2 text-danger">${wine}</h1>`
};

async function paringWine() {

    const id = $(this).data('id');
    console.log(id);
    response = await axios.get(`${BASE_API}/api/wineparing/${id}`)
    console.log(response);
    console.log(response.data.wineParing);
    if (response.data.wineParing) {
        $("#noWine").show();
        let msg = generateWineHTML_errors(response.data.wineParing);
        console.log(msg);
        $("#noWine").append(msg);
    }
    else {

        $("#winebox").show();

        for (wines of (response.data.pairedWines)) {
            let msg = generateWineHTML_tabs(wines);
            let tab_pannels = generateWineHTML_tab_pannel(wines);
            $("#myTab").append(msg);
            $("#myTabContent").append(tab_pannels);
        };
    }
}

/////////////////////////////////////////////////////////////////////////////////////


$("#myTab").on("click", ".nav-link active", searchWine);

async function searchWine() {
    const wineType = $(this).data('name');
    response = await axios.get(`${BASE_API}/searchwine/wineType`);

    for (let w_data of response.data.wines) {
        let wine = $(generateWineHTML(w_data));
        $(`#${wineType}`).append(wine);
    }

}

function generateWineHTML(wine) {
    return `<div class="col-sm-4">
             <div class="card mt-3" style:witdh=100px;>
            <img src="${wine.image}" class="card-img-top" alt="...">
            <div class="card-body text-dark">
            <ul>
            <li>${wine.title}</li>
             <li>${wine.price}</li>
            <li>Info:<br>${wine.description}</li>
            </ul>
            <a id="view-btn" type="button" class="btn btn-danger view-btn" href='${BASE_API}/recipedetail/${wine.id}' data-id=${wine.id}>View</a>
            </div>
            </div>
            </div>`;
}