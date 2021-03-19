BASE_API = "http://localhost:5000";
$(".card-body").on("click", ".view-btn", recipeDetails);

async function recipeDetails() {
    const id = $(this).data('id')
    const response = await axios.get(`${BASE_API}/recipedetail/${id}`);
    console.log(response);

}
