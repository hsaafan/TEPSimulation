from PyQt5 import QtCore, QtGui, QtWidgets


class PropertyTree(QtGui.QStandardItemModel):
    # FIXME: hardcoding parent_name
    def __init__(self, keys, headers):
        super(PropertyTree, self).__init__()
        self.data_keys = keys
        self.headers = headers
        self.setHorizontalHeaderLabels(self.headers)
        return

    def import_data(self, data):
        for item in data:
            self.add_row(item)

    def add_row(self, item):
        if len(set(self.data_keys).difference(item.keys())) > 0:
            raise RuntimeError("Data import missing keys")

        if item['parent_name'] is None:
            parent = self.invisibleRootItem()
        else:
            # Make parent uneditable
            parent = self.findItems(item['parent_name'])[0]
            i = parent.index().row()
            for j in range(len(self.data_keys) - 1):
                self.index(i, j).model().item(i, j).setEditable(False)

        new_row = []
        for key in (self.data_keys):
            if key == 'parent_name':
                continue
            new_row.append(QtGui.QStandardItem(str(item[key])))
        parent.appendRow(new_row)


class DataTrees:
    """ Data Trees Class

    Handles all data tree models in Qt application
    Attributes
    ----------

    Methods
    -------
    check_tree_exists
        Check that a tree view exists (e.g. components or reactions tree)
    check_tree_model_exists
        Check that a tree model exists (e.g. a specific component or reaction)
    set_tree_model
        Sets the model of a tree view widget to an exisiting model. If the
        model doesn't exist, it first needs to be added using add_tree_model
    add_tree_model
        Add a new tree model and set it as the current model of the tree view
    import_tree_data
        Import data into a tree model
    export_tree_data
        Export tree model data as a list
    """
    _tree_keys = {
        "components": ['parent_name', 'property_name', 'value', 'units'],
        "reactions": ['parent_name', 'property_name', 'value', 'units'],
        "units": ['parent_name', 'property_name', 'value', 'units'],
        "streams": ['parent_name', 'property_name', 'value', 'units'],
        "sensors": ['parent_name', 'property_name', 'value', 'units'],
        "disturbances": ['parent_name', 'property_name', 'value', 'units']
    }
    _tree_headers = {
        "components": ['Property', 'Value', 'Units'],
        "reactions": ['Property', 'Value', 'Units'],
        "units": ['Property', 'Value', 'Units'],
        "streams": ['Property', 'Value', 'Units'],
        "sensors": ['Property', 'Value', 'Units'],
        "disturbances": ['Property', 'Value', 'Units']
    }
    _tree_models = {
        "components": dict(),
        "reactions":  dict(),
        "units":  dict(),
        "streams": dict(),
        "sensors": dict(),
        "disturbances": dict()
    }
    _trees = None

    def __init__(self, main_ui):
        """ Connect trees and create new empty trees """
        self._trees = {
            "components": main_ui.tree_components,
            "reactions": main_ui.tree_reactions,
            "units": main_ui.tree_units,
            "streams": main_ui.tree_streams,
            "sensors": main_ui.tree_sensors,
            "disturbances": main_ui.tree_disturbances
        }
        for key in self._trees.keys():
            self.add_tree_model(key, "empty")
            self.set_tree_model(key)

    def check_tree_exists(self, tree_type: str):
        """ Check that a tree view exists """
        if tree_type not in self._trees.keys():
            raise RuntimeError(f"{tree_type} tree does not exist")

    def check_tree_model_exists(self, tree_type: str, tree_model: str):
        """ Check that a tree model exists """
        self.check_tree_exists(tree_type)
        if tree_model not in self._tree_models[tree_type].keys():
            raise RuntimeError(f"{tree_model} tree model does not exist")

    def set_tree_model(self, tree_type: str, index: str = "empty"):
        """ Set the tree model of an existing tree view"""
        self.check_tree_exists(tree_type)
        tree = self._trees[tree_type]
        tree.setModel(self._tree_models[tree_type][index])

    def add_tree_model(self, tree_type: str, index: str, data: dict = None):
        """ Create new tree model """
        self.check_tree_exists(tree_type)
        tree = PropertyTree(self._tree_keys[tree_type],
                            self._tree_headers[tree_type])

        self._tree_models[tree_type][index] = tree
        if data is not None:
            self.import_tree_data(tree_type, index, data)
        self.set_tree_model(tree_type, index)

    def import_tree_data(self, tree_type: str, index: str, data: dict):
        """ Import data into a tree model """
        self.check_tree_model_exists(tree_type, index)
        tree_model = self._tree_models[tree_type][index]
        tree_model.import_data(data)

    def export_tree_data(self, tree_type: str, index: str):
        """ Returns the data in the tree model """
        self.check_tree_model_exists(tree_type, index)
        tree_model = self._tree_models[tree_type][index]
        # TODO: export data into list
