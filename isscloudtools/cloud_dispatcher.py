from isscloudtools.initialize import get_dropbox_service, get_slack_service
from isscloudtools.dropbox import *
from isscloudtools.slack import slack_upload_image
from xas.file_io import load_binned_df_from_file
from xas.xasproject import XASDataSet
from xas.file_io import load_binned_df_from_file
import numpy as np
from matplotlib import pyplot as plt

import os

class CloudDispatcher():
    def __init__(self, dropbox_service = None,slack_service = None):
        if dropbox_service==None:
            self.dropbox_service = get_dropbox_service()
        else:
            self.dropbox_service = dropbox_service
        if slack_service==None:
            self.slack_service, self.slack_client_oath = get_slack_service()
        else:
            self.slack_service = slack_service
        self.email = ''



    def set_contact_info(self,email):
        self.email = email

    def load_to_dropbox(self,path, year = None, cycle = None, proposal = None ):
        df, header = load_binned_df_from_file(path)
        h = header.replace('#', '')
        h = h.replace('\n', ',')
        d = dict()
        for element in h.split(', '):
            if ':' in element:
                x = element.split(':')
                d[x[0]] = x[1]
        if (year is None )&(cycle is None):
            year, cycle = d['Facility.cycle'].split('-')
        if proposal is None:
            proposal = d['Facility.GUP']
        dn = '/{}/{}/{}/'.format(year, cycle, proposal).replace(' ', '')
        dropbox_upload_files(self.dropbox_service,path, dn, os.path.basename(path))

    def post_to_slack(self,path,slack_channel):
        image_path = os.path.splitext(path)[0]+'.png'
        print('image' + image_path)
        generate_output_figures(path,image_path)
        slack_upload_image(self.slack_service,
                           image_path,slack_channel,
                           os.path.basename(path).split('.')[0])





def generate_output_figures(filepath, imagepath=None, t_flag=True, f_flag=True, r_flag=True):
    plt.ioff()
    df, header = load_binned_df_from_file(filepath)
    df = df.sort_values('energy')

    energy = np.array(df['energy'])
    mu_t = np.array(np.log(df['i0']/df['it']))
    mu_f = np.array(df['iff']/df['i0'])
    mu_r = np.array(np.log(df['it']/df['ir']))
    try:
        ds_t = XASDataSet(name=filepath, md={}, energy=energy, mu=mu_t, filename=filepath, datatype='experiment')
    except:
        ds_t = None
    try:
        ds_f = XASDataSet(name=filepath, md={}, energy=energy, mu=mu_f, filename=filepath, datatype='experiment')
    except:
        ds_f = None
    try:
        ds_r = XASDataSet(name=filepath, md={}, energy=energy, mu=mu_r, filename=filepath, datatype='experiment')
    except:
        ds_r = None


    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = plt.subplots(3, 3, figsize=(12, 9))
    fig.set_tight_layout(True)

    ax_e = (ax1, ax2, ax3, ax4, ax5, ax6)
    ax_k = (ax7, ax8, ax9)
    ax_mu_raw = (ax1, ax2, ax3)
    ax_mu_flat = (ax4, ax5, ax6)
    ax_chi = (ax7, ax8, ax9)

    if t_flag:
        plot_xas_raw(energy, mu_t, ax1, color='b')
        plot_xas_in_E(ds_t, ax4, color='b')
        plot_xas_in_K(ds_t, ax7, color='b')

    if f_flag:
        plot_xas_raw(energy, mu_f, ax2, color='r')
        plot_xas_in_E(ds_f, ax5, color='r')
        plot_xas_in_K(ds_f, ax8, color='r')

    if r_flag:
        plot_xas_raw(energy, mu_r, ax3, color='k')
        plot_xas_in_E(ds_r, ax6, color='k')
        plot_xas_in_K(ds_r, ax9, color='k')


    for ax in ax_e:
        ax.set_xlabel('E, eV')
        ax.set_xlim(energy[0], energy[-1])
    for ax in ax_k:
        ax.set_xlabel('k, A$^{-1}$')
        if ds_t:
            ax.set_xlim(ds_t.k[0], ds_t.k[-1])
    for ax in ax_mu_raw:
        ax.set_ylabel('mu')
    for ax in ax_mu_flat:
        ax.set_ylabel('mu norm')
    for ax in ax_chi:
        ax.set_ylabel('$\chi$(k) * k$^{2}$')

    ax1.set_title('Transmission')
    ax2.set_title('Fluorescence')
    ax3.set_title('Reference')


    # legend = []

    #
    #
    # ax1.legend(legend)
    #
    # ax1.set_xlabel('E, eV')
    # ax1.set_ylabel('norm/flat mu')
    # ax3.set_xlabel('E, eV')
    # ax3.set_ylabel('norm/flat mu')
    # ax5.set_xlabel('E, eV')
    # ax5.set_ylabel('norm/flat mu')
    #
    # ax2.set_xlabel('k, A$^{-1}$')
    # ax2.set_ylabel('$\chi$(k) * k$^{2}$')
    # ax4.set_xlabel('k, A$^{-1}$')
    # ax4.set_ylabel('$\chi$(k) * k$^{2}$')
    # ax5.set_xlabel('k, A$^{-1}$')
    # ax6.set_ylabel('$\chi$(k) * k$^{2}$')

    # plt.tight_layout()
    if imagepath:
        plt.savefig(imagepath, dpi=300)
    plt.ion()
    plt.close(fig)


def plot_xas_raw(e, mu, ax, color):
    ax.plot(e, mu, color=color)


def plot_xas_in_E(ds, ax, color):
    if ds:
        ds.normalize_force()
        ax.plot(ds.energy, ds.flat, color=color)


def plot_xas_in_K(ds, ax, color):
    if ds:
        ds.extract_chi_force()
        ax.plot(ds.k, ds.chi * ds.k**2, color=color)



