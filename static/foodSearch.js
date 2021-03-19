BASE_API = "http://localhost:5000"

$('#search').hide();

$('#btn-search').on("click", searchFood);

async function searchFood() {

    const food = $("#recipe").val();
    const response = await axios.get(`${BASE_API}/searchrecipe/${food}`);
    console.log(response);
    $('#search').show();
    $('#search').trigger('reset');
    for (let r_data of response.data.result) {
        let recipe = $(generateRecipeHTML(r_data));
        $("#result").append(recipe)
    }
    //setInterval(recipeDeatils, 1000);
    // $("#result").append("<script src='../static/recipeDetails.js'></script>")

}

function generateRecipeHTML(recipe) {
    return `<div class="col-sm-4">
             <div class="card mt-3">
            <img src="${recipe.image}" class="card-img-top" alt="...">
            <div class="card-body text-dark">
            <ul>
            <li>${recipe.title}</li>
            <li>Ready In:${recipe.total_time}</li>
            </ul>
            <a id="view-btn" type="button" class="btn btn-danger view-btn" href='${BASE_API}/recipedetail/${recipe.id}' data-id=${recipe.id}>View</a>
            </div>
            </div>
            </div>`;
}


