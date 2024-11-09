import numpy as np
import xarray as xr

from dartsflash.pyflash import PyFlash
from dartsflash.hyflash import HyFlash


class PlotEoS:
    @staticmethod
    def pressure_volume(flash: PyFlash, temperatures: list, compositions: list, pt_props: xr.Dataset = None,
                        vt_props: xr.Dataset = None, prange: list = None, vrange: list = None):
        # Slice Dataset at composition
        comps = {comp: compositions[i] for i, comp in enumerate(flash.components[:-1])}

        # Initialize Plot object
        from dartsflash.diagram import Plot
        plot = Plot(figsize=(8, 4))
        plot.add_attributes(suptitle="PV diagram for " + flash.mixture.name,
                            ax_labels=["volume [m3/mol]", "pressure [bar]"])

        # Plot P vs. V from VT-properties
        if vt_props is not None:
            volume = vt_props.volume.values
            pressure = [vt_props.sel(comps, method='nearest').sel({"temperature": temp}, method='nearest').P.values for temp in temperatures]
            plot.draw_plot(xdata=volume, ydata=pressure, xlim=vrange, ylim=prange,
                           datalabels=['{} K'.format(temp) for temp in temperatures])

        # Plot P vs. V from PT-properties
        if pt_props is not None:
            volume = [pt_props.sel(comps, method='nearest').sel({"temperature": temp}, method='nearest').V.values for temp in temperatures]
            pressure = [pt_props.pressure.values for temp in temperatures]
            plot.draw_plot(xdata=volume, ydata=pressure, style='dashed', xlim=vrange, ylim=prange,
                           datalabels=['{} K'.format(temp) for temp in temperatures] if vt_props is None else None)
        plot.add_attributes(legend=True)

        return plot

    @staticmethod
    def compressibility(flash: PyFlash, temperatures: list, compositions: list, pt_props: xr.Dataset = None,
                        vt_props: xr.Dataset = None, zrange: list = None, prange: list = None):
        # Slice Dataset at composition
        comps = {comp: compositions[i] for i, comp in enumerate(flash.components[:-1]) if comp in pt_props.dims}

        # Initialize Plot object
        from dartsflash.diagram import Plot
        plot = Plot(figsize=(8, 4))
        plot.add_attributes(suptitle="Compressibility factor Z of " + flash.mixture.name,
                            ax_labels=["pressure [bar]", "Z, [-]"])

        # Plot Z vs. P from VT-properties
        if vt_props is not None:
            Z = [vt_props.sel(comps, method='nearest').sel({"temperature": temp}, method='nearest').Z.values for temp in temperatures]
            pressure = [vt_props.sel(comps, method='nearest').sel({"temperature": temp}, method='nearest').P.values for temp in temperatures]
            plot.draw_plot(xdata=pressure, ydata=Z, xlim=prange, ylim=zrange,
                           datalabels=['{} K'.format(temp) for temp in temperatures])

        # Plot Z vs. P from PT-properties
        if pt_props is not None:
            Z = [pt_props.sel(comps, method='nearest').sel({"temperature": temp}, method='nearest').Z.values for temp in temperatures]
            pressure = [pt_props.pressure.values for temp in temperatures]
            plot.draw_plot(xdata=pressure, ydata=Z, style="dashed", xlim=prange, ylim=zrange,
                           datalabels=['{} K'.format(temp) for temp in temperatures] if vt_props is None else None)
        plot.add_attributes(legend=True)

        return plot

    @staticmethod
    def pt(flash: PyFlash, pt_props: xr.Dataset, composition: list, props_name: dict, state: dict = None,
           cmap: str = 'winter'):
        # Slice dataset at current state
        comps = {comp: composition[i] for i, comp in enumerate(flash.components[:-1]) if comp in pt_props.dims}
        props_at_z = pt_props.sel(comps, method='nearest')
        state = state if state is not None else {"pressure": pt_props.pressure.values,
                                                 "temperature": pt_props.temperature.values}
        props_at_state = props_at_z.sel(state, method='nearest')

        # Create Diagram object
        from dartsflash.diagram import Diagram
        nplots = len(props_name)
        plot = Diagram(ncols=nplots, figsize=(nplots * 5 + 3, 5))

        assert pt_props is not None, "Please provide the PT properties to plot the enthalpy"
        for i, (prop_name, prop_title) in enumerate(props_name.items()):
            plot.subplot_idx = i
            prop_array = eval("props_at_state." + prop_name + ".T.values")

            plot.draw_surf(x=state['temperature'], y=state['pressure'], data=prop_array,
                           colours=cmap, colorbar=True, contour=True, fill_contour=True,
                           ax_labels=["temperature, K", "pressure, bar"]
                           )
            plot.add_attributes(title=prop_title + " of " + flash.mixture.name)
        return plot


class PlotPhaseDiagram:
    @staticmethod
    def binary():
        pass

    @staticmethod
    def ternary(flash: PyFlash, flash_results: xr.Dataset, x0: np.ndarray, x1: np.ndarray, state: dict, plot_tielines: bool = False):
        """
        Method to plot ternary phase diagram. The phase diagram is generated by plotting the compositions
        of the equilibrium phases at the specified feed compositions. Optional tielines connect these compositions.

        :param flash: PyFlash object
        :param flash_results: xarray.Dataset
        :param zi: np.array
        :param state: dict
        :param plot_tielines: bool
        """
        # Slice dataset at current state
        for spec in state.keys():
            state[spec] = state[spec][0] if hasattr(state[spec], "__len__") else state[spec]
        flash_at_pt = flash_results.sel(state, method='nearest')
        dz = x0[1] - x0[0]

        # Create TernaryDiagram object
        from dartsflash.diagram import TernaryDiagram
        nplots = 1
        plot = TernaryDiagram(ncols=nplots, figsize=(nplots * 5 + 3, 5), dz=dz)
        plot.add_attributes(suptitle="Phase diagram for " + flash.mixture.name + " at P = {} bar and T = {} K"
                            .format(state["pressure"], state["temperature"]))
        plot.triangulation(x0, x1, corner_labels=flash.mixture.comp_data.comp_labels)

        # Plot phase compositions xij at feed composition z
        comps = {comp: None for comp in flash.components[:-1]}
        for i, z0 in enumerate(x0):
            comps[flash.components[0]] = z0
            for j, z1 in enumerate(x1):
                comps[flash.components[1]] = z1

                # Find flash results at P,T,z
                flash_at_ptz = flash_at_pt.sel(comps, method='nearest')
                X = flash_at_ptz.X.values
                Xj = [X[jj * flash.ns:(jj + 1) * flash.ns] for jj in range(flash.np_max)]

                # For single phase conditions, skip
                if flash_at_ptz.np.values == 3:
                    plot.draw_compositions(compositions=Xj, color='b', connect_compositions=True)
                elif flash_at_ptz.np.values == 2:
                    plot.draw_compositions(compositions=Xj, color='r', connect_compositions=plot_tielines)
                else:
                    pass

        return plot

    @staticmethod
    def pt(flash: PyFlash, flash_results: xr.Dataset, compositions: list, state: dict = None,
           logx: bool = False, logy: bool = False):
        """
        Method to plot PT phase diagram at composition z. The phase diagram is generated by plotting the boundaries
        of the phase regions.

        """
        # Create Diagram object
        from dartsflash.diagram import Diagram
        nplots = 1
        plot = Diagram(ncols=nplots, figsize=(nplots * 5 + 3, 5))
        plot.add_attributes(suptitle="PT diagram for " + flash.mixture.name,
                            ax_labels=["temperature [K]", "pressure [bar]"])

        # Loop over different compositions
        compositions = [compositions] if not hasattr(compositions[0], '__len__') else compositions
        levels, _ = plot.get_levels(compositions[:][0], is_float=True, nlevels=len(compositions))
        cmap, _ = plot.get_cmap(levels)
        plot.ax[plot.subplot_idx].set_prop_cycle('color', [cmap(i) for i in np.linspace(0, 1, len(compositions))])

        for i, z in enumerate(compositions):
            # Slice dataset at current state
            comps = {comp: z[i] for i, comp in enumerate(flash.components[:-1]) if comp in flash_results.dims}
            flash_at_z = flash_results.sel(comps, method='nearest')
            state = state if state is not None else {"pressure": flash_results.pressure.values,
                                                     "temperature": flash_results.temperature.values}

            # Plot phase compositions xij at feed composition z
            T_ranges = np.empty((len(state["pressure"]), 2))
            for ii, p in enumerate(state["pressure"]):
                # Slice flash results at P,z
                np_at_pz = flash_at_z.sel({"pressure": p}, method='nearest').np.values
                T_ranges[ii, :] = None
                for j, t in enumerate(state["temperature"]):
                    if np_at_pz[j] >= 1.:
                        T_ranges[ii, 0] = t
                        break
                for jj, t in enumerate(state["temperature"][j:]):
                    if np_at_pz[j + jj] == 1.:
                        T_ranges[ii, 1] = t
                        break
                if T_ranges[ii, 0] == T_ranges[ii, 1]:
                    break

            plot.draw_line(np.append(np.append(T_ranges[:, 0], [None]), T_ranges[:, 1]),
                           np.append(np.append(state["pressure"], [None]), state["pressure"]))

        if logx:
            plot.ax[plot.subplot_idx].set_xscale("log")
        if logy:
            plot.ax[plot.subplot_idx].set_yscale("log")

        return

    @staticmethod
    def ph():
        pass


class PlotFlash:
    @staticmethod
    def solubility(flash: PyFlash, flash_results: xr.Dataset, dissolved_comp_idx: list, phase_idx: list,
                   state: dict = None, concentrations: list = None, logy: bool = False, labels: list = None, plot_1p: bool = True):
        # Slice Dataset at current state
        state = state if state is not None else {"pressure": flash_results.pressure.values,
                                                 "temperature": flash_results.temperature.values}
        flash_at_state = flash_results.sel(state, method='nearest')

        # Initialize Plot object
        from dartsflash.diagram import Plot
        dissolved_comp_idx = [dissolved_comp_idx] if not hasattr(dissolved_comp_idx, "__len__") else dissolved_comp_idx
        nplots = len(dissolved_comp_idx)
        plot = Plot(nrows=nplots, figsize=(8, nplots * 4))

        # Loop over components
        for j, idx in enumerate(dissolved_comp_idx):
            plot.subplot_idx = j
            phase_name = flash.flash_params.eos_order[phase_idx]
            dissolved_comp = flash.mixture.comp_data.comp_labels[idx]
            comp_idx = phase_idx * flash.ns + idx
            plot.add_attributes(title=dissolved_comp + " solubility in " + phase_name,
                                ax_labels=["pressure [bar]", r"x{} [-]".format(dissolved_comp)])

            np_min = 0 if plot_1p else 1
            if concentrations is not None:
                x_at_state = np.concatenate([flash_at_state.isel(concentrations=i, X_array=comp_idx).X.T.values
                                             for i, _ in enumerate(concentrations)], axis=0)
            else:
                x_at_state = flash_at_state.isel(X_array=comp_idx).X.T.values
                x_at_state = np.where(flash_at_state.np.T.values > np_min, x_at_state, np.nan)

            # Plot solubility data
            plot.draw_plot(xdata=state["pressure"], ydata=x_at_state, logy=logy, datalabels=labels)
            plot.add_attributes(legend=True, legend_loc='upper right', grid=True)

        return plot

    @staticmethod
    def binary():
        pass

    @staticmethod
    def ternary(flash: PyFlash, flash_results: xr.Dataset, dz: float, state: dict, min_z: list = None, max_z: list = None,
                composition_to_plot: list = None, plot_phase_fractions: bool = False, cmap: str = 'winter'):
        """
        Method to plot flash results
        """
        # Slice dataset at current state
        for spec in state.keys():
            state[spec] = state[spec][0] if hasattr(state[spec], "__len__") else state[spec]
        flash_at_pt = flash_results.sel(state, method='nearest')
        np_max = int(np.nanmax(flash_at_pt.np.values))

        min_z = [0., 0.] if min_z is None else min_z
        max_z = [1., 1.] if max_z is None else max_z
        x0 = np.arange(min_z[0], max_z[0]+dz*0.1, dz)
        x1 = np.arange(min_z[1], max_z[1]+dz*0.1, dz)

        # Create TernaryDiagram object
        from dartsflash.diagram import TernaryDiagram
        nplots = np_max - 1 if plot_phase_fractions else 1
        plot = TernaryDiagram(ncols=nplots, figsize=(nplots * 5 + 3, 5), dz=dz, min_z=min_z, max_z=max_z)

        if plot_phase_fractions:
            # Plot flash results at feed composition z
            for j in range(np_max - 1):
                plot.subplot_idx = j
                plot.draw_surf(x0, x1, data=flash_at_pt.nu.isel(nu_array=j).values, is_float=True, nlevels=10,
                               colours=cmap, colorbar=True, contour=False, fill_contour=True, min_val=0., max_val=1.,
                               corner_labels=flash.mixture.comp_data.comp_labels
                               )
                plot.add_attributes(title="Phase {}".format(j))
            plot.add_attributes(suptitle="Phase fraction for " + flash.mixture.name + " at P = {} bar and T = {} K"
                                .format(state["pressure"], state["temperature"]))
        else:
            # Plot np at feed composition z
            plot.subplot_idx = 0
            plot.draw_surf(x0, x1, data=flash_at_pt.np.values, is_float=False,
                           colours=cmap, colorbar=True, contour=False, fill_contour=True,
                           corner_labels=flash.mixture.comp_data.comp_labels
                           )
            plot.add_attributes(suptitle="Number of phases for " + flash.mixture.name + " at P = {} bar and T = {} K"
                                .format(state["pressure"], state["temperature"]))
        return plot

    @staticmethod
    def pt(flash: PyFlash, flash_results: xr.Dataset, composition: list, state: dict = None,
           plot_phase_fractions: bool = False, cmap: str = 'winter'):
        """ Method to plot flash results at z """
        # Slice dataset at current state
        comps = {comp: composition[i] for i, comp in enumerate(flash.components[:-1]) if comp in flash_results.dims}
        flash_at_z = flash_results.sel(comps, method='nearest')
        np_max = int(np.nanmax(flash_at_z.np.values))
        state = state if state is not None else {"pressure": flash_results.pressure.values,
                                                 "temperature": flash_results.temperature.values}

        # Create Diagram object
        from dartsflash.diagram import Diagram
        nplots = np_max - 1 if plot_phase_fractions else 1
        plot = Diagram(ncols=nplots, figsize=(nplots * 5 + 3, 5))
        plot.add_attributes(suptitle="PT diagram for " + flash.mixture.name)

        if plot_phase_fractions:
            # Plot flash results at feed composition z
            for j in range(np_max - 1):
                plot.subplot_idx = j
                plot.draw_surf(x=state["temperature"], y=state["pressure"], data=flash_at_z.sel(nu_array=j).nu.T.values,
                               ax_labels=["temperature [K]", "pressure [bar]"], is_float=True, min_val=0., max_val=1.,
                               colours=cmap, colorbar=True, contour=True, fill_contour=True, nlevels=11)
                plot.add_attributes(title="Phase {}".format(j))
        else:
            # Plot np at feed composition z
            plot.subplot_idx = 0
            plot.draw_surf(x=state["temperature"], y=state["pressure"], data=flash_at_z.np.T.values,
                           ax_labels=["temperature [K]", "pressure [bar]"], is_float=False,
                           colours=cmap, colorbar=True, contour=True, fill_contour=True)

        return plot

    @staticmethod
    def ph(flash: PyFlash, flash_results: xr.Dataset, composition: list, state: dict = None,
           pt_props: xr.Dataset = None, plot_temperature: bool = False, plot_enthalpy: bool = False, cmap: str = 'winter'):
        # Slice dataset at current state
        comps = {comp: composition[i] for i, comp in enumerate(flash.components[:-1])}
        flash_at_z = flash_results.sel(comps, method='nearest')
        state = state if state is not None else {"pressure": flash_results.pressure.values,
                                                 "enthalpy": flash_results.enthalpy.values}

        # Create Diagram object
        from dartsflash.diagram import Diagram
        nplots = 1 + plot_temperature + plot_enthalpy
        plot = Diagram(ncols=nplots, figsize=(nplots * 5 + 3, 5))
        plot.add_attributes(suptitle="PH-diagram of " + flash.mixture.name)

        # Plot phase fractions at feed composition z
        plot.subplot_idx = 0
        plot.draw_surf(x=state["enthalpy"], y=state["pressure"], data=flash_at_z.nu.isel(nu_array=0).T.values,
                       ax_labels=["enthalpy, kJ/mol", "pressure, bar"], is_float=True, min_val=0., max_val=1.,
                       colours='winter', colorbar=True, contour=True, fill_contour=True, nlevels=11)
        plot.add_attributes(title="Phase fraction, -")

        if plot_temperature:
            plot.subplot_idx += 1
            plot.draw_surf(x=state['enthalpy'], y=state['pressure'], data=flash_at_z.temp.T.values,
                           colours=cmap, colorbar=True, contour=True, fill_contour=True,
                           ax_labels=["enthalpy, kJ/mol", "pressure, bar"]
                           )
            plot.add_attributes(title="Temperature, K")

        if plot_enthalpy:
            assert pt_props is not None, "Please provide the PT properties to plot the enthalpy"
            plot.subplot_idx += 1
            state_spec = {"pressure": state['pressure'],
                          "temperature": np.linspace(np.nanmin(data), np.nanmax(data), 100)}
            data = pt_props.H_PT.values * 8.314472

            plot.draw_surf(x=state_spec['temperature'], y=state_spec['pressure'], data=data,
                           colours=cmap, colorbar=True, contour=True, fill_contour=True,
                           ax_labels=["temperature, K", "pressure, bar"]
                           )
            plot.add_attributes(title="Enthalpy, kJ/mol")
        return plot


class PlotGibbs:
    @staticmethod
    def binary(flash: PyFlash, ge_results_1p: xr.Dataset, state: dict, variable_comp_idx: int,
               flash_results: xr.Dataset = None, ge_results_np: xr.Dataset = None, composition_to_plot: list = None):
        """
        Method to plot binary GE surfaces.

        :param flash: PyFlash object
        :param ge_results_1p: xarray.DataArray
        :param state: State to plot GE surfaces for
        :param variable_comp: Index of variable component
        :param flash_results: xarray.Dataset
        :param ge_results_np: xarray.DataArray
        :param composition_to_plot: list
        """
        variable_comp = flash.components[variable_comp_idx]
        comp_str = flash.mixture.comp_data.comp_labels[variable_comp_idx]

        # Slice dataset at current state
        state_vars = {var: state[var] for var in ge_results_1p.dims if var != variable_comp}
        ge1p_at_state = ge_results_1p.sel(state_vars, method='nearest')
        zi = ge1p_at_state.variables[variable_comp].values

        # Initialize plot
        from dartsflash.diagram import Plot
        plot = Plot(figsize=(8, 4))
        plot.add_attributes(suptitle="Gibbs energy surfaces for " + flash.mixture.name + " at P = {} bar and T = {} K"
                            .format(state["pressure"], state["temperature"]))

        # Loop over EoS to plot 1P Gmix curves
        ge = [[] for _ in flash.flash_params.eos_order]
        labels = [eosname for eosname in flash.flash_params.eos_order]
        for j, eosname in enumerate(flash.flash_params.eos_order):
            ge[j] = eval("ge1p_at_state.G_PT_" + eosname + "_mix.values")
            labels += [eosname]
        plot.draw_plot(zi, ydata=ge, number_of_curves=len(ge), datalabels=labels)
        plot.add_attributes(ax_labels=[comp_str + " [-]", r"G$_{mix}$/RT"], grid=True, legend=True)

        # Plot 2P Gmix
        if flash_results is not None:
            assert composition_to_plot is not None, "Please specify a composition to plot flash results for"
            assert ge_results_np is not None, "Please provide NP phase properties"
            # Slice results at current state
            comps = {comp: composition_to_plot[i] for i, comp in enumerate(flash.components[:-1])}
            genp_at_state = ge_results_np.sel(state, method='nearest').sel(comps, method='nearest')
            flash_at_state = flash_results.sel(state, method='nearest').sel(comps, method='nearest')

            # Plot equilibrium phases
            X = [flash_at_state.X.values[j * 2] for j in range(flash.np_max)]
            Y = [genp_at_state.G_PT_mix.values[j] for j in range(flash.np_max)]
            plot.draw_point(X, Y, color='k', marker='x', point_size=30)
            plot.draw_line(X, Y, color='k', linestyle='dashed')

            # Plot composition z
            Gz = np.sum([flash_at_state.nu.values * genp_at_state.G_PT_mix.values])
            plot.draw_point(composition_to_plot, Gz, color='r', marker='x', point_size=30)

        return plot

    @staticmethod
    def ternary(flash: PyFlash, ge_results: xr.Dataset, state: dict, zi: np.ndarray,
                flash_results: xr.Dataset = None, composition_to_plot: list = None, cmap: str = 'winter'):
        """
        Method to plot ternary GE surfaces.
        """
        # Slice dataset at current state
        ge_at_pt = ge_results.sel(state, method='nearest')
        dz = zi[1] - zi[0]

        # Create TernaryDiagram object
        from dartsflash.diagram import TernaryDiagram
        nplots = len(flash.flash_params.eos_order)
        plot = TernaryDiagram(ncols=nplots, figsize=(nplots * 5 + 3, 5), dz=dz)
        plot.add_attributes(suptitle="Gibbs energy surfaces for " + flash.mixture.name + " at P = {} bar and T = {} K"
                            .format(state["pressure"], state["temperature"]))

        # Plot Gibbs energy surface of each EoS
        for j, eosname in enumerate(flash.flash_params.eos_order):
            ge = eval("ge_at_pt.G_PT_" + eosname + "_mix.values")

            plot.subplot_idx = j
            plot.draw_surf(X1=zi, X2=zi, data=ge, is_float=True, nlevels=10,
                           colours=cmap, colorbar=True, contour=True, fill_contour=True,
                           corner_labels=flash.mixture.comp_data.comp_labels
                           )

        # Plot flash results at specified composition
        if flash_results is not None:
            assert composition_to_plot is not None, "Please specify a composition to plot flash results for"
            flash_at_pt = flash_results.sel(state, method='nearest')

            # Plot phase compositions xij at feed composition z
            comps = {comp: composition_to_plot[i] for i, comp in enumerate(flash.components[:-1])}
            plot.draw_compositions(compositions=composition_to_plot, color='k')

            # Find flash results at P,T,z
            flash_at_ptz = flash_at_pt.sel(comps, method='nearest')
            X = flash_at_ptz.X.values
            Xj = [X[jj * flash.ns:(jj + 1) * flash.ns] for jj in range(flash.np_max)]

            # Plot phase compositions
            if flash_at_ptz.np.values > 1:
                plot.draw_compositions(compositions=Xj, color='r', connect_compositions=True)
            else:
                # For single phase conditions, skip
                pass

        return plot


class PlotTPD:
    @staticmethod
    def binary():
        pass

    @staticmethod
    def ternary(flash: PyFlash, tpd_results: xr.Dataset, x0, x1, state: dict,
                composition_to_plot: list = None, cmap: str = 'winter'):
        """
        Method to plot TPD

        :param flash: PyFlash object
        :param tpd_results:
        :param state:
        :param composition:
        """
        # Slice dataset at current state
        tpd_at_pt = tpd_results.sel(state, method='nearest')
        dz = x0[1] - x0[0]

        # Create TernaryDiagram object
        from dartsflash.diagram import TernaryDiagram
        nplots = 1
        plot = TernaryDiagram(ncols=nplots, figsize=(nplots * 5 + 3, 5), dz=dz)
        plot.add_attributes(suptitle="Stationary points for " + flash.mixture.name + " at P = {} bar and T = {} K"
                            .format(state["pressure"], state["temperature"]))

        # Plot number of negative TPD
        ntpd = tpd_at_pt.neg_sp.values
        plot.draw_surf(X1=x0, X2=x1, data=ntpd, is_float=False,
                       colours=cmap, colorbar=True, contour=True, fill_contour=True,
                       corner_labels=flash.mixture.comp_data.comp_labels
                       )

        # Plot TPD at composition
        if composition_to_plot is not None:
            assert len(composition_to_plot) == flash.ns
            comps = {comp: composition_to_plot[i] for i, comp in enumerate(flash.components[:-1])}

            Y = tpd_at_pt.sel(comps, method='nearest').y.values
            Ysp = [Y[j * flash.ns:(j + 1) * flash.ns] for j in range(flash.np_max)]
            plot.draw_compositions(compositions=composition_to_plot, color='k')
            plot.draw_compositions(compositions=Ysp, color='r', connect_compositions=True)

        return plot

    @staticmethod
    def pt():
        pass

    @staticmethod
    def xy():
        pass


class PlotHydrate:
    @staticmethod
    def pt(flash: HyFlash, flash_results: xr.Dataset, compositions_to_plot: list, state: dict = None,
           concentrations: list = None, labels: list = None, ref_t: list = None, ref_p: list = None, logy: bool = False,
           props: xr.Dataset = None, legend_loc: str = 'upper right'):
        # Slice Dataset at state and composition
        state = state if state is not None else {"pressure": flash_results.pressure.values,
                                                 "temperature": flash_results.temperature.values}
        results_at_state = flash_results.sel(state, method='nearest')

        # Initialize Plot object
        from dartsflash.diagram import Plot
        plot = Plot(figsize=(8, 4))
        plot.add_attributes(suptitle=flash.mixture.name + "-hydrate", ax_labels=["temperature", "pressure"])

        # Loop over compositions
        comps = {comp: compositions_to_plot[i] for i, comp in enumerate(flash.components[:-1]) if comp in flash_results.dims}
        results_at_comp = results_at_state.sel(comps, method='nearest')

        # If multiple salt concentrations have been specified, concatenate
        if results_at_comp.pressure.values[0] is None:
            if concentrations is not None:
                X_at_state = np.concatenate([results_at_comp.isel(concentrations=i).pres.values
                                             for i, _ in enumerate(concentrations)], axis=0)
            else:
                X_at_state = results_at_comp.pres.values
        else:
            if concentrations is not None:
                X_at_state = np.concatenate([results_at_comp.isel(concentrations=i).temp.T.values
                                             for i, _ in enumerate(concentrations)], axis=0)
            else:
                X_at_state = results_at_comp.temp.values

        # Plot equilibrium curve data
        if results_at_comp.pressure.values[0] is None:
            pressure = X_at_state
            temperature = results_at_comp.temperature.values
        else:
            pressure = results_at_comp.pressure.values
            temperature = X_at_state

        plot.draw_plot(xdata=temperature, ydata=pressure, logy=logy, datalabels=labels)
        if ref_t is not None or ref_p is not None:
            plot.draw_refdata(xref=ref_t, yref=ref_p)
        plot.add_attributes(legend=labels is not None, legend_loc=legend_loc, grid=True)

        return

    @staticmethod
    def binary(flash: HyFlash, flash_results: xr.Dataset, state: dict = None, compositions: list = None):
        return
