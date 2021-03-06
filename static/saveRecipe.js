BASE_API = "https://thousandrecipes.herokuapp.com/";
//BASE_API="http://localhost:5000"

$("#winebox").hide();
$("#noWine").hide();

$(".card-body").on("click", "#wine-btn", paringWine);

function generateWineHTML_tabs(wine) {

    return ` <li class="nav-item" role="presentation">
            <a class="nav-link " id="${wine}-tab" data-bs-toggle="tab" data-bs-target="#${wine}" type="button"
                role="tab" aria-controls="${wine}" aria-selected="true" data-id="${wine}">${wine}</a>
        </li>`;

}

function generateWineHTML_tab_pannel(wine) {
    return `
         <div class="tab-pane fade " id="${wine}" role="tabpanel" aria-labelledby="${wine}-tab">...</div>
        `;
}

function generateWineHTML_errors(wine) {
    return `<h1 class="display-2 text-danger">${wine}</h1>`
};

async function paringWine() {

    const id = $(this).data('id');
    console.log(id);
    response = await axios.get(`${BASE_API}/api/wine/wineparing/${id}`)
    console.log(response);
    console.log(response.data.wineParing);
    if (response.data.wineParing) {
        $("#noWine").show();
        let msg = generateWineHTML_errors(response.data.wineParing);
        console.log(msg);
        $("#noWine").append(msg);
        $("#wine-btn").hide();
    }
    else {

        $("#winebox").show();

        for (wines of (response.data.pairedWines)) {
            let msg = generateWineHTML_tabs(wines);
            let tab_pannels = generateWineHTML_tab_pannel(wines);
            $("#myTab").append(msg);
            $("#myTabContent").append(tab_pannels);
            break;
        };

        $("#wine-btn").hide();
    }
}

/////////////////////////////////////////////////////////////////////////////////////


$("#myTab").on("click", ".nav-item", searchWine);

async function searchWine() {

    const wineType = $(this).children().data("id");
    const response = await axios.get(`${BASE_API}/api/winesearchwine/${wineType}`);
    for (let w_data of response.data.wines) {
        let wine = generateWineHTML(w_data);
        $("#wines").append(wine);
        
    }

}

function generateWineHTML(wine) {
    return `<div class="col-sm-4 items" style=" height: fitcontent ;" >
             <div class="card mt-3" >
            <img src="${wine.image}" class="card-img-top" alt="..." style="height:200px">
            <div class="card-body text-dark">
            <ul>
            <li>${wine.title}</li>
             <li>${wine.price}</li>
           
            </ul>
             <p>Info:<br>${wine.description}</p>
           
            </div>
            </div>
            </div>`;
    
}