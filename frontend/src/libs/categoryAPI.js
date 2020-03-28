import api from "@/libs/api";

export default {
  getCategories() {
    return api
      .get(`/categories`)
      .then(response => response.data)
      .catch(error => {
        console.log(error);
      });
  }
};
