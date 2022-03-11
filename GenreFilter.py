import pdb


def main(String):
    Genre=list(String.split("'"))
    filteredgenres=list(filter(filtergenres,Genre))
    print(filteredgenres)
    return(filteredgenres)



def filtergenres(Genre):
    ListofGenres=["Action", "Drama", "Comedy", "Romance", "Crime", "Adventure", "Science Fiction"]
    return True if Genre in ListofGenres else False





 