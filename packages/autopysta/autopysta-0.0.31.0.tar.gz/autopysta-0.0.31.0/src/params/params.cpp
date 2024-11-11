#include "params/params.h"
#include <iostream>

params_cust::params_cust() : map() {}  // Initializes the unordered_map

void params_cust::add(const std::string& nuevo_nombre, double nuevo_valor) {
    map[nuevo_nombre] = nuevo_valor;  // Directly insert into unordered_map
}

double params_cust::get(const std::string& nombre) const {
    auto it = map.find(nombre);
    if (it != map.end()) {
        return it->second;
    }
    return 0;  // Return 0 if key is not found
}

params::params() {}
