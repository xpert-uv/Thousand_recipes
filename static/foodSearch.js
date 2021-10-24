//BASE_API = "https://thousandrecipes.herokuapp.com/";
BASE_API = "http://localhost:5000/api/";
$('#search').hide();
$("#page-btn").hide()
$('#btn-search').on("click", searchFood);

async function searchFood() {

    const food = $("#recipe").val();
   // const fixedFood = food.replace("","%");
    const response = await axios.get(`${BASE_API}/recipe/search/${food}`);
    $('#search').show();
    $('#search').trigger('reset');
    $("#result").empty();
    if (response.data.result.length === 0) {
        $("#result").append(generateErrorMessage)
    }
    for (let r_data of response.data.result) {
        let recipe = $(generateRecipeHTML(r_data));
       $("#result").append(recipe);
    }

    //Pagination
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

function generateRecipeHTML(recipe) {
    return `<div class="col-sm-4 items" style="height:400px">
             <div class="card mt-3">
            <img src="${recipe.image}" class="card-img-top" alt="..." style="height:200px">
            <div class="card-body text-dark">
            <ul>
            <li>${recipe.title}</li>
            <li>Ready In:${recipe.total_time}</li>
            </ul>
            <a id="view-btn" type="button" class="btn btn-danger view-btn" href='${BASE_API}/recipe/detail/${recipe.id}' data-id=${recipe.id}>View</a>
            </div>
            </div>
            </div>`;
}


const generateErrorMessage = () => {
    return `<div>
        <h1> No recipe Found.</h1>
    </div>`
    
};