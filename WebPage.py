import importlib
import os
from bottle import template, route, run, static_file, error
from Models.Logging import log
from Models.SQLhandler import SQLHandler
import const


def response_template(data=[], description='', code=700):
    status = True if len(data) > 0 else False
    template_data = {
        'status': status,
        'description': description,
        "code": code,
        "data": data
    }
    return template_data


@route('/')
def index():
    dictionary = {"categories": select_form_database()}
    return template('template', name='Romek', wordList=dictionary)


@error(404)
def error404(error):
    return response_template(description='<h1>error 404</h1>', code=404)


@route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root='static')


def select_form_database():
    sql_handler = SQLHandler()
    x = sql_handler.select('SELECT sensor_name, sensor_data, sensor_date  FROM sensor_records LIMIT 100')
    return x


@route('/<controlerName>/<actionName>', ['GET', 'POST'])
def global_router(controlerName='index', actionName='index'):
    file_path = os.path.join(os.getcwd(), 'controllers')
    # lista plikow w katalogu
    file_name = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))]
    # lista nazw z katalou bez Controller.py
    file_name_cut = ' '.join(file_name).replace('Controller.py', '').split()

    if controlerName in file_name_cut:
        controller_path = controlerName + 'Controller.py'
        controller_full_name = controlerName + 'Controller'

        if os.path.isfile(os.path.join(os.getcwd(), 'controllers', controller_path)):
            module_name = 'controllers.' + controller_full_name
            module = importlib.import_module(module_name, package=controller_full_name)
            controller_instance = getattr(module, controller_full_name)()

            if not hasattr(controller_instance, '__class__'):
                log.debug('Controller {} nie posiada klasy o takiej samej nazwie'.format(controller_full_name))
            action_full_name = actionName + '_action'

            if hasattr(controller_instance, action_full_name):
                log.debug('Controller {} posiada akcje {}'.format(controller_full_name, actionName))

                controller_action = getattr(controller_instance, actionName + '_action')

                if callable(controller_action):
                    log.debug('Controller {}, posiada akcje {}, ktora moze byc wywolana'.format(controller_full_name,
                                                                                                actionName))
                    response = controller_action()
                    if not isinstance(response, list):
                        response = [response]
                    return response_template(description='istnieje strona {}/{}'.format(controlerName, actionName),
                                             data=response)
                else:
                    log.debug('Controller {}, nie posiada akcji {}, jest to atrybut '.format(controller_full_name,
                                                                                             actionName))
            else:
                print 'Controller {} nie posiada akcji {}'.format(controller_full_name, actionName)

                return response_template(description='nie istnieje strona {}/{}'.format(controlerName, actionName),
                                         data=[actionName])

            return response_template(description='istnieje strona {}/{}'.format(controlerName, actionName),
                                     data=[actionName])
        else:
            print ('Controller o takiej nazwie nie istnieje: [{}]'.format(controlerName))
    else:
        return response_template(description='nie istnieje strona {}/{}'.format(controlerName, actionName),
                                 data=[actionName])


run(host=const.SERVERURL, port=const.SERVERPORT, debug=True, reloader=True)
