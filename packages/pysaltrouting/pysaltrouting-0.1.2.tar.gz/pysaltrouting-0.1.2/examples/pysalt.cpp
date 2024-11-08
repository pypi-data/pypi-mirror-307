#include <pybind11/pybind11.h>
#include "salt/salt.h"
#include "salt/base/eval.h"
#include "salt/base/flute/flute.h"
#include <string>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;

void net_file(const std::string& netFile, double eps, const std::string& postfile, const std::string powvfile) {
    // TODO: ASSIGN FILE TO C GLOBAL VAR
    if (postfile != "") {
        flute::POSTFILE_PATH = new char[postfile.length() + 1];
        strcpy(flute::POSTFILE_PATH, postfile.c_str());
    }
    if (powvfile != "") {
        flute::POWVFILE_PATH = new char[powvfile.length() + 1];
        strcpy(flute::POWVFILE_PATH, powvfile.c_str());
    }
    salt::Net net;
    net.Read(netFile);
    printlog("Run SALT algorithm on net", net.name, "with", net.pins.size(), "pins using epsilon =", eps);

    // Run SALT
    salt::Tree tree;
    salt::SaltBuilder saltB;
    saltB.Run(net, tree, eps);

    // Report
    printlog("Tree topology is as follows:");
    cout << tree;
    salt::WireLengthEval eval(tree);
    printlog("Wire length is", eval.wireLength);
    printlog("Max path length is", eval.maxPathLength);
    printlog("Avg path length is", eval.avgPathLength);
    printlog("Max stretch (shallowness) is", eval.maxStretch);
    printlog("Avg stretch is", eval.avgStretch);
    tree.Write("SALT");
}

PYBIND11_MODULE(pysalt, m) {
    m.doc() = "python binding for salt";
    m.def("net_file", &net_file, "routing net file", py::arg("netFile"), py::arg("eps") = 1.101, py::arg("postfile") = "", py::arg("powvfile") = "");
#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
} 
