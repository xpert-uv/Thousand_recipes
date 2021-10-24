//BASE_API = "https://thousandrecipes.herokuapp.com/";
BASE_API = "http://localhost:5000/api/";
$('#search').hide();

$('#btn-search').on("click", searchWine);

async function searchWine() {

    const wine = $("#wine").val();
    const response = await axios.get(`${BASE_API}/wine/searchwine/${wine}`);
    console.log(response);
    $('#search').show();
    $('#search').trigger('reset');
    $("#result").empty();

     if (response.data.result.length === 0) {
        $("#result").append(generateErrorMessage)
    }

    for (let w_data of response.data.wines) {
        let wine = $(generateWineHTML(w_data));
        $("#result").append(wine)
    }
    

     $("#page-btn").show()
    $("#page-btn > ul").empty();
    const totalItem = $("#result > .items").length;
    const limitPerPage = 10;
    $("#result > .items:gt(" + (limitPerPage - 1) + ")").hide();
    const pageNums = Math.round(totalItem / limitPerPage);

    //$(".pagination").append(` <li class="page-item"><a class="page-link" href="javascript:void(0)">Previous</a></li>`);
    //$(".pagination").append(`<li><a  class="page-link current-page active" href="javascript:void(0)" data-id="1">${1}</a></li>`);

    for (let i = 1; i <= pageNums; i++){
       $(".pagination").append(`<li><a class="page-link current-page" href="javascript:void(0)" data-id=${i}>${i}</a></li>`);
        
    }
    //$(".pagination").append(`<li class="page-item"><a class="page-link" href="javascript:void(0)">Next</a></li>`)

    $(".pagination").on("click", ".current-page", function () {
        if ($(this).hasClass("active")) {
            return false;
        } else {
            let currentPage = $(this).data("id");
            $("#result > .items").hide();

            const grandTotal = currentPage * limitPerPage;
            for (let i = grandTotal - limitPerPage; i < grandTotal; i++){
                $("#result > .items:eq(" + (i) + ")").show();
            }
       
        }
        
    })
}

function generateWineHTML(wine) {
    return `<div class="col-sm-4" style="height:400px" >
             <div class="card mt-3" >
            <img src="${wine.image}" class="card-img-top" alt="..." style="height:200px">
            <div class="card-body text-dark">
            <ul>
            <li>${wine.title}</li>
             <li>${wine.price}</li>
            <li>Info:<br>${wine.description}</li>
            </ul>
           
            </div>
            </div>
            </div>`;
    
}

const generateErrorMessage = () => {
    return `<div>
        <h1> No recipe Found.</h1>
    </div>`

}
