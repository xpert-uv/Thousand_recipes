BASE_API = "https://thousandrecipes.herokuapp.com/";
$(".card-body").on("click", ".view-btn", recipeDetails);

async function recipeDetails() {
    const id = $(this).data('id')
    const response = await axios.get(`${BASE_API}/recipedetail/${id}`);
    

}
